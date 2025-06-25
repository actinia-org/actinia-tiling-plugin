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

from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
import pickle
from uuid import uuid4
from copy import deepcopy

from actinia_processing_lib.persistent_processing import PersistentProcessing
from actinia_rest_lib.resource_base import ResourceBase
from actinia_core.core.common.kvdb_interface import enqueue_job
from actinia_core.core.common.process_chain import ProcessChainConverter

from actinia_tiling_plugin.apidocs import tiling
from actinia_tiling_plugin.resources.processes import pctpl_to_pl
from actinia_tiling_plugin.models.response_models.tiling import \
    GridTilingResponseModel


class AsyncTilingProcessGridResource(ResourceBase):
    """Create grid tiles.
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
            # processing = AsyncTilingProcessGrid(rdc)
            # processing.run()
            enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(tiling.grid_tiling_post_docs)
    def post(self, project_name, mapset_name):
        """Create grid tiles.
        """
        self._execute(project_name, mapset_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)

    @swagger.doc(tiling.grid_tiling_get_docs)
    def get(self, project_name, mapset_name):
        """Get description of the grid tiling process.
        """
        process_desc = deepcopy(tiling.grid_tiling_post_docs)
        del process_desc["responses"]
        process_desc["process_results"] = dict()
        process_desc["process_results"]["type"] = "array"
        process_desc["process_results"]["items"] = "string"
        process_desc["process_results"]["description"] = \
            "List of the vector names of the created grid tiles."
        return make_response(jsonify(process_desc), 200)


def start_job(*args):
    processing = AsyncTilingProcessGrid(*args)
    processing.run()


class AsyncTilingProcessGrid(PersistentProcessing):
    """Create a grid.
    """

    def __init__(self, *args):
        PersistentProcessing.__init__(self, *args)
        self.response_model_class = GridTilingResponseModel

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

    def _execute(self):

        grid_step_num = 2
        post_step_num = 1
        self.progress["step"] = grid_step_num + post_step_num

        self._execute_preparation()
        pconv = ProcessChainConverter()

        # v.mkgrid with output map and box
        req_data_orig = self.request_data
        grid_prefix = req_data_orig["grid_prefix"]
        grid_name = f"grid_{uuid4().hex}"
        box = f"{req_data_orig['width']},{req_data_orig['height']}"
        tpl_values1 = {"grid_name": grid_name, "box": box}
        pl1, pconv = pctpl_to_pl("pc_create_grid.json", tpl_values1)
        self.output_parser_list = pconv.output_parser_list
        self._execute_process_list(pl1)
        self._parse_module_outputs()
        grid_info = self.module_results["grid_info"]
        num_grid_cells = int([
            info.split("=")[1] for info in grid_info
            if info.split("=")[0] == "centroids"
        ][0])
        num_of_steps = grid_step_num
        self.progress["num_of_steps"] = num_of_steps
        self.progress["step"] = grid_step_num + post_step_num + num_grid_cells

        # extract grid cells
        grid_data = list()
        zp_len = len(str(num_grid_cells))
        text = "{:0%s}" % zp_len
        grid_data = [
            {"cat": cat, "zeropaddedcat": text.format(cat)}
            for cat in range(1, num_grid_cells + 1)
        ]
        tpl_values2 = {
            "grid_name": grid_name,
            "grid_prefix": grid_prefix,
            "data": grid_data,
            # "n": num_grid_cells,
        }
        pl2, _ = pctpl_to_pl("pc_extract_grid.json", tpl_values2)
        self._execute_process_list(pl2)
        num_of_steps += num_grid_cells
        self.progress["num_of_steps"] = num_of_steps
        self.progress["step"] = grid_step_num + post_step_num + num_grid_cells

        # delete grid
        tpl_values3 = {"vector_name": grid_name}
        pl3, _ = pctpl_to_pl("pc_delete_vector.json", tpl_values3)
        self._execute_process_list(pl3)

        self._execute_finalization()
        num_of_steps += post_step_num
        self.progress["num_of_steps"] = num_of_steps
        self.progress["step"] = grid_step_num + post_step_num + num_grid_cells

        # make response pretty
        self.module_results = list()
        for val in grid_data:
            self.module_results.append(f"{grid_prefix}{val['zeropaddedcat']}")
