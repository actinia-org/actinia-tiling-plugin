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

Hello World grid tiling
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import json
import pytest
from flask import Response

from actinia_core.core.common.app import URL_PREFIX

from ..testsuite import ActiniaTestCase


class GridTilingTest(ActiniaTestCase):

    location = "nc_spm_08"
    mapset = "tiling_test_mapset"
    base_url = f"{URL_PREFIX}/locations/{location}/mapsets/{mapset}"
    content_type = "application/json"

    mapset_created = False

    def tearDown(self):
        if self.mapset_created is True:
            rv = self.app.delete(
                URL_PREFIX + '/locations/%s/mapsets/%s/lock'
                             % (self.location, self.mapset),
                headers=self.admin_auth_header)
            self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
            rv2 = self.app.delete(
                URL_PREFIX + '/locations/%s/mapsets/%s' % (self.location, self.mapset),
                headers=self.admin_auth_header)
            self.waitAsyncStatusAssertHTTP(rv2, headers=self.admin_auth_header)
        else:
            self.__class__.mapset_created = True
        self.app_context.pop()

    @pytest.mark.integrationtest
    def test_get_grid_apidocs(self):
        """Test the get method of tiling grid endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.location)

        url = f"{URL_PREFIX}/locations/{self.location}/mapsets"
        resp = self.app.get(URL_PREFIX + "/locations", headers=self.user_auth_header)
        import pdb; pdb.set_trace()

        # assert type(resp) is Response, "The response is not of type Response"
        # assert resp.status_code == 200, "The status code is not 200"
        # assert hasattr(resp, "json"), "The response has no attribute 'json'"
        # assert "message" in resp.json, (
        #     "There is no 'message' inside the " "response"
        # )
        # assert resp.json["message"] == "Hello world!", (
        #     "The response message" " is wrong"
        # )

    # @pytest.mark.integrationtest
    # def test_post_helloworld(self):
    #     """Test the post method of the /helloworld endpoint"""
    #     postbody = {"name": "test"}
    #     resp = self.app.post(
    #         URL_PREFIX + "/helloworld",
    #         headers=self.user_auth_header,
    #         data=json.dumps(postbody),
    #         content_type="application/json",
    #     )
    #     assert type(resp) is Response, "The response is not of type Response"
    #     assert resp.status_code == 200, "The status code is not 200"
    #     assert hasattr(resp, "json"), "The response has no attribute 'json'"
    #     assert "message" in resp.json, (
    #         "There is no 'message' inside the " "response"
    #     )
    #     assert resp.json["message"] == "Hello world TEST!", (
    #         "The response " "message is wrong"
    #     )
    #
    # @pytest.mark.integrationtest
    # def test_post_helloworld_error(self):
    #     """Test the post method of the /helloworld endpoint"""
    #     postbody = {"namee": "test"}
    #     resp = self.app.post(
    #         URL_PREFIX + "/helloworld",
    #         headers=self.user_auth_header,
    #         data=json.dumps(postbody),
    #         content_type="application/json",
    #     )
    #     assert type(resp) is Response, "The response is not of type Response"
    #     assert resp.status_code == 400, "The status code is not 400"
    #     assert resp.data == b"Missing name in JSON content"
