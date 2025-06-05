#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Grid Tiling Class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

from copy import deepcopy
import re
import os

from uuid import uuid4
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
import pickle


from actinia_core.core.common.config import global_config
from actinia_processing_lib.persistent_processing import PersistentProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_core.processing.actinia_processing.persistent.mapset_management \
    import (
        PersistentMapsetDeleter,
        PersistentMapsetUnlocker,
    )

from actinia_tiling_plugin.apidocs import merge
from actinia_tiling_plugin.resources.processes import pctpl_to_pl
from actinia_tiling_plugin.models.response_models.tiling import \
    GridTilingResponseModel
from actinia_tiling_plugin.resources.logging import log


class AsyncMergeProcessPatchResource(ResourceBase):
    """Merging mapsets with same raster, vector maps and strds in one mapset by
    patching the maps.
    """

    def _execute(self, project_name, mapset_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            project_name=project_name,
            mapset_name=mapset_name,
        )
        if rdc:
            # # for debugging use the following lines instead of enqueue_job
            # processing = AsyncMergeProcessPatch(rdc)
            # processing.run()
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(merge.patch_merge_post_docs)
    def post(self, project_name, mapset_name):
        """Merging mapsets with same raster, vector, ... maps in one mapset by
        patching the maps.
        """
        self._execute(project_name, mapset_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)

    @swagger.doc(merge.patch_merge_get_docs)
    def get(self, project_name, mapset_name):
        """Get description of the patch merge process.
        """
        process_desc = deepcopy(merge.patch_merge_post_docs)
        del process_desc["responses"]

        io_parameter_base_schema = dict()
        io_parameter_base_schema["type"] = "array"
        io_parameter_base_schema["items"] = "object with properties 'param' "\
            "and 'value'."
        del process_desc["parameters"][1]["schema"]
        process_desc["parameters"][1]["schema"] = io_parameter_base_schema
        process_desc["parameters"][1]["description"] = (
            "A list of data to patch in the new mapset. The 'param' must "
            "be on of 'vector', 'raster' or 'strds' and the 'value' is a "
            "string of the maps which should be patched."
        )
        return make_response(jsonify(process_desc), 200)


def start_job(*args):
    processing = AsyncMergeProcessPatch(*args)
    processing.run()


class AsyncMergeProcessPatch(PersistentProcessing):
    """Create a grid.
    """

    def __init__(self, *args):
        PersistentProcessing.__init__(self, *args)
        self.response_model_class = GridTilingResponseModel
        self.num_of_steps = 0
        self.num_steps = {
            "raster": [2],
            "vector": [3],
            "strds": [3, 2],
            "stvds": [0],
        }
        self.step = 0
        self.raster_maps = list()
        self.vector_maps = list()
        self.strds = list()
        self.strds_infos = dict()
        self.stvds = list()
        for output in self.request_data["outputs"]:
            if output["param"] == "raster":
                self.raster_maps = output["value"].split(",")
            elif output["param"] == "vector":
                self.vector_maps = output["value"].split(",")
            elif output["param"] == "strds":
                self.strds = output["value"].split(",")
            # elif output["param"] == "stvds":
            #     self.stvds = output["value"].split(",")
            else:
                log.info(f"Output type '{output['param']}' not yet supported!")
            self.step += (
                sum(self.num_steps[output["param"]]) * len(
                    output["value"].split(","))
            )
        self.mapsetlist = self.request_data["mapsetlist"]

    def _execute_preparation(self):

        self._setup()

        # Check and lock the target and temp mapsets
        self._check_lock_target_mapset()

        if self.target_mapset_exists is False:
            # Create the temp database and link the
            # required mapsets into it
            self._create_temp_database(self.required_mapsets)

            # Initialize the GRASS environment and switch into PERMANENT
            # mapset, which is always linked
            self._create_grass_environment(
                grass_data_base=self.temp_grass_data_base,
                mapset_name="PERMANENT"
            )

            # Create the temporary mapset with the same name as the target
            # mapset and switch into it
            self._create_temporary_mapset(
                temp_mapset_name=self.target_mapset_name,
                interim_result_mapset=None,
                interim_result_file_path=None)
            self.temp_mapset_name = self.target_mapset_name
        else:
            # Init GRASS environment and create the temporary mapset
            self._create_temporary_grass_environment(
                source_mapset_name=self.target_mapset_name)
            self._lock_temp_mapset()

    def _execute_finalization(self):
        # Copy local mapset to original project, merge mapsets
        self._copy_merge_tmp_mapset_to_target_mapset()

    def _generate_name_mapset_str(self, name):
        name_list = list()
        for mapset in self.mapsetlist:
            name_list.append(f"{name}@{mapset}")
        return ",".join(name_list)

    def _set_progress(self):
        self.progress["step"] = self.step
        self.progress["num_of_steps"] = self.num_of_steps

    def _delete_mapset(self, mapset_name):
        if mapset_name != "PERMANENT":
            rdc_delete = deepcopy(self.rdc)
            rdc_delete.mapset_name = mapset_name
            unlocker = PersistentMapsetUnlocker(rdc_delete)
            unlocker._execute()
            mapset_deleter = PersistentMapsetDeleter(rdc_delete)
            mapset_deleter._execute()

    def _patch_raster(self, rast):
        # patch raster map
        tpl = "patch/pc_patch_raster.json"
        rasterlist = self._generate_name_mapset_str(rast)
        tpl_rpatch = {
            "rasterlist": rasterlist,
            "raster": rast,
        }
        plr, _ = pctpl_to_pl(tpl, tpl_rpatch)
        self._execute_process_list(plr)
        self.num_of_steps += self.num_steps["raster"][0]
        self._set_progress()

    def _patch_vector(self, vect):
        # check for attribute table
        tpl_check = "patch/pc_vector_check_attrtable.json"
        tpl_check_val = {"map": vect}
        plcheck, pconv = pctpl_to_pl(tpl_check, tpl_check_val)
        self.output_parser_list = pconv.output_parser_list
        self._execute_process_list(plcheck)
        self._parse_module_outputs()
        attrcheck = self.module_results["attrtable"]
        attributetable = False if attrcheck[0] == "" else True
        # patch vector maps
        tpl = "patch/pc_patch_vector.json"
        vectorlist = self._generate_name_mapset_str(vect)
        tpl_vpatch = {
            "vectorlist": vectorlist,
            "vector": vect,
            "attributetable": attributetable,
        }
        plv, _ = pctpl_to_pl(tpl, tpl_vpatch)
        self._execute_process_list(plv)
        self.num_of_steps += self.num_steps["vector"][0]
        self._set_progress()

    def _prepare_patch_strds(self):
        """Prepares the patch of STRDS by reading one STRDS and adding the
        rasters to the list of rasters to patch and writing other information
        to the dict self.strds_infos.
        """
        for strds in self.strds:
            # strds get list of rasters and other STRDS infos
            tpl_values_strds = {"strds": f"{strds}@{self.mapsetlist[0]}"}
            pl_strds, pconv = pctpl_to_pl(
                "patch/pc_strds_list_rasters.json", tpl_values_strds)
            self.output_parser_list = pconv.output_parser_list
            self._execute_process_list(pl_strds)
            self._parse_module_outputs()
            strds_rasters = self.module_results["rasters"]
            strds_desc = self.module_results["strds_description"]
            strds_info = self.module_results["strds_info"]
            col_names = strds_rasters[0].split("|")
            strds_raster_infos = dict()
            strds_raster_infos["rasters"] = list()
            for idx in range(1, len(strds_rasters)):
                rast_info = dict()
                rinfos = strds_rasters[idx].split("|")
                for j in range(len(rinfos)):
                    rast_info[col_names[j]] = rinfos[j]
                rast_info["all"] = strds_rasters[idx]
                strds_raster_infos["rasters"].append(rast_info)
                if rast_info["name"] not in self.raster_maps:
                    self.raster_maps.append(rast_info["name"])
            desc = "".join([entry[2:] if entry not in [
                "# Title:", "# Description:", "# Command history:"] else entry
                for entry in strds_desc])
            strds_raster_infos["title"] = re.findall(
                r"# Title:(.*?)# Description:", desc
            )[0]
            strds_raster_infos["description"] = re.findall(
                r"# Description:(.*?)# Command history:", desc
            )[0]
            strds_raster_infos["temporaltype"] = strds_info["temporal_type"]
            strds_raster_infos["semantictype"] = strds_info["semantic_type"]
            self.strds_infos[strds] = strds_raster_infos
            self.num_of_steps += self.num_steps["strds"][0]
            self.step += (
                self.num_steps["raster"][0] * len(
                    strds_raster_infos["rasters"]
                )
            )
            self._set_progress()

    def _patch_strds(self, strds_name, strds_info):
        """Creates new STRDS as a duplicate with patched rasters.
        """
        id = str(uuid4())
        tmp_strds_file = os.path.join(
            global_config.TMP_WORKDIR, f"strds_{strds_name}_{id}.txt"
        )
        # write file to register the rasters in the STRDS without the mapset
        with open(tmp_strds_file, "w") as f:
            for rast in strds_info["rasters"]:
                r_info = rast["all"].replace(
                    f"{self.mapsetlist[0]}|", ""
                )
                f.write(r_info + "\n")
        tpl_values_strds_create = {
            "strds": f"{strds_name}",
            "temporaltype": strds_info["temporaltype"],
            "semantictype": strds_info["semantictype"],
            "description": strds_info["description"],
            "title": strds_info["title"],
            "file": tmp_strds_file,
        }
        pl_strds_c, _ = pctpl_to_pl(
            "patch/pc_strds_create.json", tpl_values_strds_create)
        self._execute_process_list(pl_strds_c)
        os.remove(tmp_strds_file)
        self.num_of_steps += self.num_steps["strds"][1]
        self._set_progress()

    def _execute(self):

        keep_mapsets = self.request_data["keep_mapsets"]
        self.required_mapsets.extend(self.mapsetlist)

        self._execute_preparation()
        self._set_progress()

        self._prepare_patch_strds()
        for rast in self.raster_maps:
            self._patch_raster(rast)
        for vect in self.vector_maps:
            self._patch_vector(vect)
        # create new STRDS as a duplicate with patched rasters
        for strds_name, strds_info in self.strds_infos.items():
            self._patch_strds(strds_name, strds_info)

        # TODO STVDS

        # delete temporary mapsets
        if keep_mapsets is not True and keep_mapsets.lower() != "true":
            for mapset_name in self.mapsetlist:
                self._delete_mapset(mapset_name)

        self._execute_finalization()

        # make response pretty
        self.module_results = list()
