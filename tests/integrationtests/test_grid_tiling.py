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

Tests for tiling grid endpoints
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pytest
from flask import Response

from ..test_resource_base import URL_PREFIX
from ..test_resource_base import ActiniaResourceTestCaseBase

# PC_SET_REGION = """{
#   "list": [
#     {
#       "id": "set_region_for_epsg25832",
#       "module": "g.region",
#       "inputs": [
#         {
#           "param": "vector",
#           "value": "boundary_county@PERMANENT"
#         },
#         {
#           "param": "res",
#           "value": "100000"
#         }
#       ],
#       "flags": "a"
#     }
#   ],
#   "version": "1"
# }"""

PC_TILING_GRID = """{
  "width": "0.5",
  "height": "0.5",
  "grid_prefix": "grid"
}"""


class GridTilingTest(ActiniaResourceTestCaseBase):

    location = "nc_spm_08"
    mapset = "tiling_test_mapset"
    base_url = f"{URL_PREFIX}/locations/{location}/mapsets/{mapset}"
    content_type = "application/json"

    mapset_created = False

    def tearDown(self):
        if self.mapset_created is True:
            rv = self.server.delete(
                URL_PREFIX
                + "/locations/%s/mapsets/%s/lock"
                % (self.location, self.mapset),
                headers=self.admin_auth_header,
            )
            self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
            rv2 = self.server.delete(
                URL_PREFIX
                + "/locations/%s/mapsets/%s" % (self.location, self.mapset),
                headers=self.admin_auth_header,
            )
            self.waitAsyncStatusAssertHTTP(rv2, headers=self.admin_auth_header)
        else:
            self.__class__.mapset_created = True
        self.app_context.pop()

    @pytest.mark.integrationtest
    def test_get_grid_apidocs(self):
        """Test the get method of tiling grid endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)

        url = f"{self.base_url}/tiling_processes/grid"
        resp = self.server.get(url, headers=self.user_auth_header)

        # assert type(resp) is Response, "The response is not of type Response"
        print(type(resp))
        assert resp.status_code == 200, "The status code is not 200"
        assert "description" in resp.json, "No 'description' in response"
        assert "parameters" in resp.json, "No 'parameters' in response"
        assert (
            "process_results" in resp.json
        ), "No 'process_results' in response"
        assert "tags" in resp.json, "No 'tags' in response"
        assert resp.json["tags"] == ["Tiling"], "'tags' are wrong"
        param_names = list()
        for param in resp.json["parameters"]:
            param_names.append(param["name"])
        param_names.sort()
        assert param_names == [
            "grid_prefix",
            "height",
            "width",
        ], "Parameter names are wrong"

    @pytest.mark.integrationtest
    def test_post_grid_apidocs(self):
        """Test the post method of tiling grid endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)

        # TODO setting the region does not work for me
        # # set region (5x9 cells)
        # rv = self.server.post(
        #     f"{self.base_url}/processing_async",
        #     headers=self.user_auth_header,
        #     content_type=self.content_type,
        #     data=PC_SET_REGION,
        # )
        # resp = self.waitAsyncStatusAssertHTTP(
        #     rv,
        #     headers=self.user_auth_header,
        #     http_status=200,
        #     status="finished",
        # )
        # url = f"{self.base_url}/info"
        # resp = self.server.get(url, headers=self.user_auth_header)

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
        assert resp2["process_results"] == ["grid1", "grid2", "grid3", "grid4"]
