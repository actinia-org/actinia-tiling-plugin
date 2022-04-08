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

Hello World grid tiling
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pytest
from flask import Response
from jinja2 import Template

from ..test_resource_base import URL_PREFIX
from ..test_resource_base import ActiniaResourceTestCaseBase


PC_TILING_GRID = """{
  "width": "0.5",
  "height": "0.5",
  "grid_prefix": "grid"
}"""

PC_TPL_COMPUTING_ON_TILES = """{
  "list": [
    {
      "id": "set_region_for_grid",
      "module": "g.region",
      "inputs": [
        {
          "param": "vector",
          "value": "{{ grid }}"
        },
        {
          "param": "res",
          "value": "0.1"
        }
      ],
      "flags": "pa"
    },
    {
      "id": "random_ndvi_raster",
      "module": "r.surf.random",
      "inputs": [
        {
          "param": "min",
          "value": "0"
        },
        {
          "param": "max",
          "value": "200"
        }
      ],
      "outputs": [
        {
          "param": "output",
          "value": "ndvi"
        }
      ],
      "flags": "i"
    },
    {
      "id": "random_ndwi_raster",
      "module": "r.surf.random",
      "inputs": [
        {
          "param": "min",
          "value": "0"
        },
        {
          "param": "max",
          "value": "1"
        }
      ],
      "outputs": [
        {
          "param": "output",
          "value": "ndwi"
        }
      ],
      "flags": "i"
    },
    {
      "id": "random_test_vector_points",
      "module": "v.random",
      "inputs": [
        {
          "param": "npoints",
          "value": "3"
        }
      ],
      "outputs": [
        {
          "param": "output",
          "value": "points"
        }
      ]
    },
    {
      "id": "random_test_vector_aras",
      "module": "v.buffer",
      "inputs": [
        {
          "param": "input",
          "value": "points"
        },
        {
          "param": "distance",
          "value": "0.1"
        }
      ],
      "outputs": [
        {
          "param": "output",
          "value": "areas"
        }
      ]
    }
  ],
  "version": "1"
}"""

PC_MERGE_PATCH = """{
  "mapsetlist": ["merge_test_mapset_tmp_grid1", "merge_test_mapset_tmp_grid2", "merge_test_mapset_tmp_grid3", "merge_test_mapset_tmp_grid4"],
  "outputs":[
    {"param": "raster", "value": "ndvi,ndwi"},
    {"param": "vector", "value": "points,areas"}
  ],
  "keep_mapsets": {{ keep_mapsets }}
}"""


class PatchMergeTest(ActiniaResourceTestCaseBase):

    location = "nc_spm_08"
    mapset = "merge_test_mapset"
    base_url = f"{URL_PREFIX}/locations/{location}/mapsets/{mapset}"
    content_type = "application/json"
    grids = ["grid1", "grid2", "grid3", "grid4"]
    created_mapsets = list()

    @classmethod
    def setUpClass(cls):
        super(PatchMergeTest, cls).setUpClass()
        accessible_datasets = {"nc_spm_08": ["PERMANENT"]}
        cls.user_id, cls.user_group, cls.user_auth_header = cls.create_user(
            name="user", role="user", process_num_limit=30,
            process_time_limit=400, accessible_datasets=accessible_datasets)

    def delete_mapset(self, mapset_name):
        rv = self.server.delete(
            URL_PREFIX
            + "/locations/%s/mapsets/%s/lock"
            % (self.location, mapset_name),
            headers=self.admin_auth_header,
        )
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
        rv2 = self.server.delete(
            URL_PREFIX
            + "/locations/%s/mapsets/%s" % (self.location, mapset_name),
            headers=self.admin_auth_header,
        )
        self.waitAsyncStatusAssertHTTP(rv2, headers=self.admin_auth_header)

    def tearDown(self):
        for mapset in self.created_mapsets:
            import pdb; pdb.set_trace()
            self.delete_mapset(mapset)
        self.created_mapsets = list()
        self.app_context.pop()

    @pytest.mark.integrationtest
    def test_get_grid_apidocs(self):
        """Test the get method of merge patch endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)
        self.created_mapsets.append(self.mapset)

        url = f"{self.base_url}/merge_processes/patch"
        resp = self.server.get(url, headers=self.user_auth_header)

        assert type(resp) is Response, "The response is not of type Response"
        assert resp.status_code == 200, "The status code is not 200"
        assert "description" in resp.json, "No 'description' in response"
        assert "parameters" in resp.json, "No 'parameters' in response"
        assert "tags" in resp.json, "No 'tags' in response"
        assert resp.json["tags"] == ["Merge"], "'tags' are wrong"
        param_names = list()
        for param in resp.json["parameters"]:
            param_names.append(param["name"])
        param_names.sort()
        assert param_names == [
            "keep_mapsets",
            "mapsetlist",
            "outputs",
        ], "Parameter names are wrong"

    def create_grid(self):
        # create grid
        url = f"{self.base_url}/tiling_processes/grid"
        rv2 = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=PC_TILING_GRID,
        )
        resp2 = self.waitAsyncStatusAssertHTTP(
            rv2,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        assert "process_results" in resp2, "No 'process_results' in response"
        assert resp2["process_results"] == self.grids

    def compute_in_tmp_mapsets(self):
        # compute raster and vector maps in temporary mapsets on different
        # tiles
        procs = list()
        for grid in self.grids:
            proc = dict()
            proc["tpl"] = Template(PC_TPL_COMPUTING_ON_TILES)
            proc["pc"] = proc["tpl"].render(grid=f"{grid}@{self.mapset}")
            proc["url"] = f"{self.base_url}_tmp_{grid}/processing_async"
            self.created_mapsets.append(f"{self.mapset}_tmp_{grid}")
            proc["rv"] = self.server.post(
                proc["url"],
                headers=self.user_auth_header,
                content_type=self.content_type,
                data=proc["pc"],
            )
            proc["resp"] = self.waitAsyncStatusAssertHTTP(
                proc["rv"],
                headers=self.user_auth_header,
                http_status=200,
                status="finished",
            )
            procs.append(proc)
            del proc

    @pytest.mark.integrationtest
    def test_post_grid_keeping_mapsets(self):
        """Test the post method of tiling grid endpoint keeping the mapsets"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)
        self.created_mapsets.append(self.mapset)

        self.create_grid()
        self.compute_in_tmp_mapsets()

        # merge
        url = f"{self.base_url}/merge_processes/patch"
        tpl = Template(PC_MERGE_PATCH)
        pc = tpl.render(keep_mapsets=True)
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=pc,
        )
        resp = self.waitAsyncStatusAssertHTTP(
            rv,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )

        # check mapsets
        mapset_url = f"{URL_PREFIX}/locations/{self.location}/mapsets"
        rv_mapset = self.server.get(
            mapset_url,
            headers=self.user_auth_header,
        )
        resp_mapset = self.waitAsyncStatusAssertHTTP(
            rv_mapset,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        for mapset in self.created_mapsets:
            assert mapset in resp_mapset["process_results"], \
                f"Mapset '{mapset}' not in list."

        # check raster
        raster_url = f"{self.base_url}/raster_layers"
        rv_raster = self.server.get(
            raster_url,
            headers=self.user_auth_header,
        )
        resp_raster = self.waitAsyncStatusAssertHTTP(
            rv_raster,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        for rast in ["ndvi", "ndwi"]:
            assert rast is resp_raster["process_results"], \
                f"Raster '{rast}' not in list."

        # check vector
        raster_url = f"{self.base_url}/vector_layers"
        rv_raster = self.server.get(
            raster_url,
            headers=self.user_auth_header,
        )
        resp_raster = self.waitAsyncStatusAssertHTTP(
            rv_raster,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        for vect in ["areas", "points"]:
            assert vect is resp_raster["process_results"], \
                f"Vector '{vect}' not in list."


    @pytest.mark.integrationtest
    def test_post_grid_deleting_mapsets(self):
        """Test the post method of tiling grid endpoint deleting the mapsets"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)
        self.created_mapsets.append(self.mapset)

        self.create_grid()
        self.compute_in_tmp_mapsets()

        # merge
        url = f"{self.base_url}/merge_processes/patch"
        tpl = Template(PC_MERGE_PATCH)
        pc = tpl.render(keep_mapsets=False)
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=pc,
        )
        resp = self.waitAsyncStatusAssertHTTP(
            rv,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )

        # check mapsets
        mapset_url = f"{URL_PREFIX}/locations/{self.location}/mapsets"
        rv_mapset = self.server.get(
            mapset_url,
            headers=self.user_auth_header,
        )
        resp_mapset = self.waitAsyncStatusAssertHTTP(
            rv_mapset,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        import pdb; pdb.set_trace()
        for mapset in self.created_mapsets:
            assert mapset in resp_mapset["process_results"], \
                f"Mapset '{mapset}' not in list."

        # check raster
        raster_url = f"{self.base_url}/raster_layers"
        rv_raster = self.server.get(
            raster_url,
            headers=self.user_auth_header,
        )
        resp_raster = self.waitAsyncStatusAssertHTTP(
            rv_raster,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        for rast in ["ndvi", "ndwi"]:
            assert rast is resp_raster["process_results"], \
                f"Raster '{rast}' not in list."

        # check vector
        raster_url = f"{self.base_url}/vector_layers"
        rv_raster = self.server.get(
            raster_url,
            headers=self.user_auth_header,
        )
        resp_raster = self.waitAsyncStatusAssertHTTP(
            rv_raster,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        for vect in ["areas", "points"]:
            assert vect is resp_raster["process_results"], \
                f"Vector '{vect}' not in list."
