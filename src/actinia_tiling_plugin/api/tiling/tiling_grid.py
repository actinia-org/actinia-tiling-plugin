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
from jinja2 import Template
import json
from flask import make_response, jsonify
from flask_restful_swagger_2 import Resource
from flask_restful_swagger_2 import swagger
import pickle
from uuid import uuid4

from actinia_core.core.common.app import auth
from actinia_core.core.common.api_logger import log_api_call
from actinia_core.rest.persistent_processing import PersistentProcessing
from actinia_core.rest.resource_base import ResourceBase
from actinia_core.core.common.redis_interface import enqueue_job
from actinia_core.core.common.app import URL_PREFIX

from actinia_core.rest.mapset_management import MapsetManagementResourceUser

from actinia_tiling_plugin.apidocs import helloworld
from actinia_tiling_plugin.resources.templating import tplEnv


class AsyncTilingProcessGridResource(ResourceBase):
    """Sample a STRDS at vector point locations, asynchronous call
    """

    def _execute(self, location_name, mapset_name):

        rdc = self.preprocess(
            has_json=True,
            has_xml=False,
            location_name=location_name,
            mapset_name=mapset_name,
        )
        if rdc:
            processing = AsyncTilingProcessGrid(rdc)
            processing.run()
            # enqueue_job(self.job_timeout, start_job, rdc)

        return rdc

    @swagger.doc(helloworld.describeHelloWorld_post_docs)
    def post(self, location_name, mapset_name):
        """Sample a strds by point coordinates, asynchronous call
        """
        self._execute(location_name, mapset_name)
        html_code, response_model = pickle.loads(self.response_data)
        return make_response(jsonify(response_model), html_code)

    # def get(self):
    # TODO


def start_job(*args):
    processing = AsyncTilingProcessGrid(*args)
    processing.run()


class AsyncTilingProcessGrid(PersistentProcessing):
    """Create a grid.
    """

    def __init__(self, *args):
        PersistentProcessing.__init__(self, *args)
        # TODO RESPONSEMODEL
        # self.response_model_class = STRDSSampleGeoJSONResponseModel

    def _execute(self):
        self._setup()

        # mapset_mr = MapsetManagementResourceUser()
        # mapset_resp = mapset_mr.get(self.location_name, self.mapset_name)
        # mapset_info = json.loads(mapset_resp.data)["process_results"]

        # v.mkgrid with output map and box
        req_data = self.request_data
        grid_prefix = req_data["grid_prefix"]
        grid_name = f"grid_{uuid4().hex}"
        box = f"{req_data['width']},{req_data['height']}"
        self.request_data = {
            "list": [
                {
                     "id": "create_grid",
                     "module": "v.mkgrid",
                     "inputs": [
                         {
                             "param": "box",
                             "value": box
                         }
                     ],
                     "outputs": [
                         {
                             "param": "map",
                             "value": grid_name
                         }
                     ]
                },
                {
                     "id": "grid_info",
                     "module": "v.info",
                     "inputs": [
                         {
                             "param": "map",
                             "value": grid_name
                         }
                     ],
                     "flags": "t",
                     "stdout": {
                        "id": "grid_info",
                        "format": "list",
                        "delimiter": "|"}
                }
            ],
            "version": "1"
        }
        PersistentProcessing._execute(self, skip_permission_check=True)
        grid_info = self.module_results["grid_info"]
        num_grid_cells = int([
            info.split("=")[1] for info in grid_info
            if info.split("=")[0] == "centroids"
        ][0])

        # extract grid cells
        extract_pc = {"list": [], "version": "1"}
        # v.extract input=hpdagrid out=hodagrid1 cat=1
        tpl_path = 'pc_extract_grid.json'
        import pdb; pdb.set_trace()
        tplEnv.list_templates()
        import pdb; pdb.set_trace()
        tpl = tplEnv.get_template(tpl_path)

        self.request_data = json.loads(tpl.render(
            grid_name=grid_name,
            grid_prefix=grid_prefix,
            n=num_grid_cells
        ).replace('\n', '').replace(" ", ""))
        # for num in range(1, num_grid_cells + 1):
        #     print(num)
        #     proc = deepcopy(extract_proc)
        #     proc["inputs"][1]["value"] = str(num)
        #     proc["outputs"][0]["value"] = f"{grid_prefix}{num}"
        #     extract_pc["list"].append(proc)
        #     del proc
        # self.request_data = extract_pc


        # delete grid

        # make response pretty



        # point_file = tempfile.NamedTemporaryFile(dir=self.temp_file_path, delete=True)
        # result_file = tempfile.NamedTemporaryFile(dir=self.temp_file_path, delete=True)
        #
        # point_file.write(json_dumps(geojson).encode())
        # point_file.flush()
        #
        # pc = dict()
        # pc["1"] = {"module": "v.import",
        #            "inputs": {"input": point_file.name},
        #            "outputs": {"output": {"name": "input_points"}}}
        #
        # pc["2"] = {"module": "t.rast.sample",
        #            "inputs": {"strds": "%s@%s" % (strds_name, self.mapset_name),
        #                       "points": "input_points"},
        #            "outputs": {"output": {"name": result_file.name}},
        #            "flags": "rn",
        #            "overwrite": True,
        #            "verbose": True}
        #
        # self.request_data = pc
        #
        # # Run the process chain
        # PersistentProcessing._execute(self, skip_permission_check=True)
        #
        # result = open(result_file.name, "r").readlines()
        #
        # output_list = []
        # for line in result:
        #     output_list.append(line.strip().split("|"))
        #
        # self.module_results = output_list
        #
        # point_file.close()
        # result_file.close()

# class TilingProcessGridResource(PersistentProcessing):
#
#     def __init__(self, *args):
#         PersistentProcessing.__init__(self, *args)
#         self.response_model_class = STRDSSampleGeoJSONResponseModel
#
#     def post(self, location_name, mapset_name):
#         """Create a grid.
#         """
#
#
#     decorators = [log_api_call, auth.login_required]


# region ist vorher gesetzt
# POSTBODY
# {
#   width: .., # in map unitx
#   height: ..,
#   output_prefix: ..,
# }
# RESP
# [
#   output_prefix1,
#   output_prefix2,
#   output_prefix3,
#   ...
# ]
