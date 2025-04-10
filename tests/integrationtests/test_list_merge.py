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

Tests for merge list endpoint
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pytest

from actinia_core.version import init_versions, G_VERSION

from ..test_resource_base import URL_PREFIX
from ..test_resource_base import ActiniaResourceTestCaseBase


class ListMergeTest(ActiniaResourceTestCaseBase):

    project_url_part = "projects"

    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()
    grass_version_s = G_VERSION["version"]
    grass_version = [int(item) for item in grass_version_s.split(".")[:2]]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    project = "nc_spm_08"
    mapset = "merge_test_mapset"
    base_url = f"{URL_PREFIX}/{project_url_part}/{project}/mapsets/{mapset}"
    content_type = "application/json"

    mapset_created = False

    def tearDown(self):
        if self.mapset_created is True:
            rv = self.server.delete(
                f"{URL_PREFIX}/{self.project_url_part}/{self.project}/mapsets/"
                "{self.mapset}/lock",
                headers=self.admin_auth_header,
            )
            self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)
            rv2 = self.server.delete(
                f"{URL_PREFIX}/{self.project_url_part}/{self.project}/mapsets/"
                "{self.mapset}",
                headers=self.admin_auth_header,
            )
            self.waitAsyncStatusAssertHTTP(rv2, headers=self.admin_auth_header)
        else:
            self.__class__.mapset_created = True
        self.app_context.pop()

    @pytest.mark.integrationtest
    def test_get_merge_apidocs(self):
        """Test the get method of list merge processes endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.project)

        url = f"{self.base_url}/merge_processes"
        resp = self.server.get(url, headers=self.user_auth_header)

        assert resp.status_code == 200, "The status code is not 200"
        assert "merge_processes" in resp.json[0], \
            "No 'merge_processes' in response"
        assert "categories" in resp.json[0]["merge_processes"][0], \
            "No 'categories' in merge process response"
        assert "description" in resp.json[0]["merge_processes"][0], \
            "No 'description' in merge process response"
        assert "id" in resp.json[0]["merge_processes"][0], \
            "No 'id' in merge process response"
