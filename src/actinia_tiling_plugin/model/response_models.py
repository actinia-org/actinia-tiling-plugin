#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018-present mundialis GmbH & Co. KG

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

from actinia_core.models.response_models import ProcessingResponseModel


class SimpleStatusCodeResponseModel(Schema):
    """Simple response schema to inform about status."""

    type = "object"
    properties = {
        "status": {
            "type": "number",
            "description": "The status code of the request.",
        },
        "message": {
            "type": "string",
            "description": "A short message to describes the status",
        },
    }
    required = ["status", "message"]


simpleResponseExample = SimpleStatusCodeResponseModel(
    status=200, message="success"
)
SimpleStatusCodeResponseModel.example = simpleResponseExample


class GridTilingResponseModel(ProcessingResponseModel):
    """Grid tiling response schema."""
    type = "object"
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = {}
    properties["process_results"]["type"] = "array"
    properties["process_results"]["items"] = "string"
    properties["process_results"]["description"] = (
        "The names of all created tiles."
    )
    example = {
      "accept_datetime": "2022-03-18 07:07:47.549554",
      "accept_timestamp": 1647587267.5495534,
      "api_info": {
        "endpoint": "asynctilingprocessgridresource",
        "method": "POST",
        "path": "/api/v2/locations/loc_25832/mapsets/hpda_tiling_user9/tiling_processes/grid",
        "request_url": "http://localhost:8088/api/v2/locations/loc_25832/mapsets/hpda_tiling_user9/tiling_processes/grid"
      },
      "datetime": "2022-03-18 07:07:58.073407",
      "http_code": 200,
      "message": "Processing successfully finished",
      "process_chain_list": [],
      "process_log": [
        {
          "executable": "v.mkgrid",
          "id": "create_grid",
          "mapset_size": 35511,
          "parameter": [
            "box=4000,4000",
            "map=grid_e36bc9d7246143f08805e8bc34561af5"
          ],
          "return_code": 0,
          "run_time": 0.10036396980285645,
          "stderr": [
            "Writing out vector rows...",
            "0..20..40..60..80..100",
            "Writing out vector columns...",
            "0..14..28..42..57..71..85..100",
            "Creating centroids...",
            "0..25..50..75..100",
            "Building topology for vector map <grid_e36bc9d7246143f08805e8bc34561af5@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..3..5..8..10..12..15..17..20..22..24..27..29..31..34..36..39..41..43..46..48..50..53..55..58..60..62..65..67..70..72..74..77..79..81..84..86..89..91..93..96..98..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..4..8..12..16..20..25..29..33..37..41..45..50..54..58..62..66..70..75..79..83..87..91..95..100",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.info",
          "id": "grid_info",
          "mapset_size": 35511,
          "parameter": [
            "map=grid_e36bc9d7246143f08805e8bc34561af5",
            "-t"
          ],
          "return_code": 0,
          "run_time": 0.10032224655151367,
          "stderr": [
            ""
          ],
          "stdout": "nodes=35\npoints=0\nlines=0\nboundaries=58\ncentroids=24\nareas=24\nislands=1\nprimitives=82\nmap3d=0\n"
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 51606,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=1",
            "output=grid1"
          ],
          "return_code": 0,
          "run_time": 0.10039615631103516,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid1@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 67701,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=2",
            "output=grid2"
          ],
          "return_code": 0,
          "run_time": 0.1004338264465332,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid2@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 83796,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=3",
            "output=grid3"
          ],
          "return_code": 0,
          "run_time": 0.10038948059082031,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid3@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 99891,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=4",
            "output=grid4"
          ],
          "return_code": 0,
          "run_time": 0.10041260719299316,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid4@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 115986,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=5",
            "output=grid5"
          ],
          "return_code": 0,
          "run_time": 0.10045146942138672,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid5@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 132081,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=6",
            "output=grid6"
          ],
          "return_code": 0,
          "run_time": 0.10038948059082031,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid6@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 148176,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=7",
            "output=grid7"
          ],
          "return_code": 0,
          "run_time": 0.10038971900939941,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid7@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 164271,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=8",
            "output=grid8"
          ],
          "return_code": 0,
          "run_time": 0.10045981407165527,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid8@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 180366,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=9",
            "output=grid9"
          ],
          "return_code": 0,
          "run_time": 0.10042524337768555,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid9@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 196465,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=10",
            "output=grid10"
          ],
          "return_code": 0,
          "run_time": 0.10045099258422852,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid10@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 212564,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=11",
            "output=grid11"
          ],
          "return_code": 0,
          "run_time": 0.10036182403564453,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid11@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 228663,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=12",
            "output=grid12"
          ],
          "return_code": 0,
          "run_time": 0.1004791259765625,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid12@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 244762,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=13",
            "output=grid13"
          ],
          "return_code": 0,
          "run_time": 0.10027718544006348,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid13@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 260861,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=14",
            "output=grid14"
          ],
          "return_code": 0,
          "run_time": 0.10032296180725098,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid14@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 276960,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=15",
            "output=grid15"
          ],
          "return_code": 0,
          "run_time": 0.1003880500793457,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid15@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 293059,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=16",
            "output=grid16"
          ],
          "return_code": 0,
          "run_time": 0.1004793643951416,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid16@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 309158,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=17",
            "output=grid17"
          ],
          "return_code": 0,
          "run_time": 0.10033535957336426,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid17@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 325257,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=18",
            "output=grid18"
          ],
          "return_code": 0,
          "run_time": 0.15061712265014648,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid18@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 341356,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=19",
            "output=grid19"
          ],
          "return_code": 0,
          "run_time": 0.1004641056060791,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid19@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 357455,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=20",
            "output=grid20"
          ],
          "return_code": 0,
          "run_time": 0.15067052841186523,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid20@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 373554,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=21",
            "output=grid21"
          ],
          "return_code": 0,
          "run_time": 0.10046601295471191,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid21@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 389653,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=22",
            "output=grid22"
          ],
          "return_code": 0,
          "run_time": 0.15063023567199707,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid22@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 405752,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=23",
            "output=grid23"
          ],
          "return_code": 0,
          "run_time": 0.10042500495910645,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid23@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "v.extract",
          "id": "",
          "mapset_size": 421851,
          "parameter": [
            "input=grid_e36bc9d7246143f08805e8bc34561af5",
            "cat=24",
            "output=grid24"
          ],
          "return_code": 0,
          "run_time": 0.10036969184875488,
          "stderr": [
            "Extracting features...",
            "2..6..9..12..15..18..21..24..28..31..34..37..40..43..46..50..53..56..59..62..65..68..71..74..78..81..84..87..90..93..96..100",
            "Building topology for vector map <grid24@mapset_9fe8aa3a786e47df820308d23ae9f275>...",
            "Registering primitives...",
            "",
            "Building areas...",
            "0..25..50..75..100",
            "Attaching islands...",
            "0..100",
            "Attaching centroids...",
            "0..100",
            "Writing attributes...",
            ""
          ],
          "stdout": ""
        },
        {
          "executable": "g.remove",
          "id": "delete_vector",
          "mapset_size": 386822,
          "parameter": [
            "type=vector",
            "name=grid_e36bc9d7246143f08805e8bc34561af5",
            "-f"
          ],
          "return_code": 0,
          "run_time": 0.10029029846191406,
          "stderr": [
            "Removing vector <grid_e36bc9d7246143f08805e8bc34561af5>",
            ""
          ],
          "stdout": ""
        }
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
        "grid24"
      ],
      "progress": {
        "num_of_steps": 0,
        "step": 27
      },
      "resource_id": "resource_id-29d78154-ce5b-4162-b883-2858a660c421",
      "status": "finished",
      "time_delta": 10.523866176605225,
      "timestamp": 1647587278.0734034,
      "urls": {
        "resources": [],
        "status": "http://localhost:8088/api/v2/resources/actinia-gdi/resource_id-29d78154-ce5b-4162-b883-2858a660c421"
      },
      "user_id": "actinia-gdi"
    }
