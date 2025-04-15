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

Response models
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from copy import deepcopy
from flask_restful_swagger_2 import Schema

from actinia_api import URL_PREFIX
from actinia_core.models.response_models import ProcessingResponseModel


class TilingShortDescResponseModel(Schema):
    """Response schema for short description of tiling processes."""
    type = "object"
    properties = {
        "categories": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Categories of the process."
        },
        "description": {
            "type": "string",
            "description": "Description of the process."
        },
        "id": {
            "type": "string",
            "description": "ID of the process."
        }
    }
    required = ["categories", "id", "description"]
    example = {
        "tiling_processes": [
            {
                "categories": ["Tiling"],
                "description": "Creates grid tiles with a speciefied "
                "'width' and 'height' in the current computational region."
                " The created grids have the given 'grid_prefix' and will "
                "be listed in the 'process_results'. Minimum required "
                "user role: user.",
                "id": "grid"
            }
        ]
    }


class TilingListResponseModel(Schema):
    """Tiling process list reponse schema."""
    type = "object"
    properties = {
        "tiling_processes": {
            "type": "array",
            "items": {"type": TilingShortDescResponseModel},
            "description": "The list of all available tiling processes."
        }
    }
    required = ["tiling_processes"]
    example = [
        {
            "tiling_processes": [
                {
                    "categories": ["Tiling"],
                    "description": "Creates grid tiles with a speciefied "
                    "'width' and 'height' in the current computational region."
                    " The created grids have the given 'grid_prefix' and will "
                    "be listed in the 'process_results'. Minimum required "
                    "user role: user.",
                    "id": "grid"
                }
            ]
        },
        200
    ]


class GridTilingResponseModel(ProcessingResponseModel):
    """Grid tiling response schema."""

    type = "object"
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = "string"
    properties["process_results"][
        "description"
    ] = "The names of all created tiles."
    example = {
        "accept_datetime": "2022-03-18 07:21:38.154889",
        "accept_timestamp": 1647588098.154888,
        "api_info": {
            "endpoint": "asynctilingprocessgridresource",
            "method": "POST",
            "path": f"{URL_PREFIX}/projects/loc_25832/mapsets/tiling_"
            "user/tiling_processes/grid",
            "request_url": f"http://localhost:8088{URL_PREFIX}/projects/"
            "loc_25832/mapsets/tiling_user/tiling_processes/grid",
        },
        "datetime": "2022-03-18 07:21:48.784597",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [],
        "process_log": [
            {
                "executable": "v.mkgrid",
                "id": "create_grid",
                "mapset_size": 35519,
                "parameter": [
                    "box=4000,4000",
                    "map=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1003878116607666,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.info",
                "id": "grid_info",
                "mapset_size": 35519,
                "parameter": [
                    "map=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "-t",
                ],
                "return_code": 0,
                "run_time": 0.10044622421264648,
                "stderr": [""],
                "stdout": "nodes=35\npoints=0\nlines=0\nboundaries=58\n"
                "centroids=24\nareas=24\nislands=1\nprimitives=82\nmap3d=0\n",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 51630,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=1",
                    "output=grid1",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10028576850891113,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 67741,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=2",
                    "output=grid2",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10046982765197754,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 83852,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=3",
                    "output=grid3",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10047054290771484,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 99963,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=4",
                    "output=grid4",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1005702018737793,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 116074,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=5",
                    "output=grid5",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10041236877441406,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 132185,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=6",
                    "output=grid6",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10047578811645508,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 148296,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=7",
                    "output=grid7",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10039210319519043,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 164407,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=8",
                    "output=grid8",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10032200813293457,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 180518,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=9",
                    "output=grid9",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10045933723449707,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 196633,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=10",
                    "output=grid10",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10046982765197754,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 212748,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=11",
                    "output=grid11",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10045719146728516,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 228863,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=12",
                    "output=grid12",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10044598579406738,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 244978,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=13",
                    "output=grid13",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10049009323120117,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 261093,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=14",
                    "output=grid14",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10048079490661621,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 277208,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=15",
                    "output=grid15",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10041666030883789,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 293323,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=16",
                    "output=grid16",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10049557685852051,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 309438,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=17",
                    "output=grid17",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10041141510009766,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 325553,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=18",
                    "output=grid18",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1003267765045166,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 341668,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=19",
                    "output=grid19",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10041117668151855,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 357783,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=20",
                    "output=grid20",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.15062570571899414,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 373898,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=21",
                    "output=grid21",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1004018783569336,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 390013,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=22",
                    "output=grid22",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.1506185531616211,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 406128,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=23",
                    "output=grid23",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.15079355239868164,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "v.extract",
                "id": "",
                "mapset_size": 422243,
                "parameter": [
                    "input=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "cat=24",
                    "output=grid24",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10039138793945312,
                "stderr": [""],
                "stdout": "",
            },
            {
                "executable": "g.remove",
                "id": "delete_vector",
                "mapset_size": 387206,
                "parameter": [
                    "type=vector",
                    "name=grid_66fce2f6f4474641b97ebad81b3c9c71",
                    "-f",
                    "--qq",
                ],
                "return_code": 0,
                "run_time": 0.10044646263122559,
                "stderr": [""],
                "stdout": "",
            },
        ],
        "process_results": [
            "grid1",
            "grid2",
            "grid3",
            "grid4",
            "grid5",
            "grid6",
            "grid7",
            "grid8",
            "grid9",
            "grid10",
            "grid11",
            "grid12",
            "grid13",
            "grid14",
            "grid15",
            "grid16",
            "grid17",
            "grid18",
            "grid19",
            "grid20",
            "grid21",
            "grid22",
            "grid23",
            "grid24",
        ],
        "progress": {"num_of_steps": 0, "step": 27},
        "resource_id": "resource_id-4f3d98a7-ac54-40ef-ad71-d790c012aed2",
        "status": "finished",
        "time_delta": 10.62972092628479,
        "timestamp": 1647588108.7845933,
        "urls": {
            "resources": [],
            "status": f"http://localhost:8088{URL_PREFIX}/resources/actinia-"
            "gdi/resource_id-4f3d98a7-ac54-40ef-ad71-d790c012aed2",
        },
        "user_id": "actinia-gdi",
    }
