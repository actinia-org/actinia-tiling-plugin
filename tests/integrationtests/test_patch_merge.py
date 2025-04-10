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

Tests for patch merge endpoints
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


import pytest
from flask.json import loads as json_loads
from jinja2 import Template

from actinia_core.version import init_versions, G_VERSION

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
      "id": "random_ndvi_1_raster",
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
          "value": "ndvi_1"
        }
      ],
      "flags": "i"
    },
    {
      "id": "random_ndvi_2_raster",
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
          "value": "ndvi_2"
        }
      ],
      "flags": "i"
    },
    {
      "id": "random_ndvi_3_raster",
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
          "value": "ndvi_3"
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
      "id": "ndvi_strds_create",
      "module": "t.create",
      "inputs": [
        {
          "param": "type",
          "value": "strds"
        },
        {
          "param": "description",
          "value": "example strds"
        },
        {
          "param": "title",
          "value": "example_strds"
        }
      ],
      "outputs": [
        {
          "param": "output",
          "value": "ndvi"
        }
      ]
    },
    {
      "id": "ndvi_strds_register",
      "module": "t.register",
      "inputs": [
        {
          "param": "input",
          "value": "ndvi"
        },
        {
          "param": "maps",
          "value": "ndvi_1,ndvi_2,ndvi_3"
        },
        {
          "param": "start",
          "value": "2022-01-01"
        },
        {
          "param": "increment",
          "value": "1 months"
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
  "mapsetlist": ["merge_test_mapset_tmp_grid1", "merge_test_mapset_tmp_grid2",
  "merge_test_mapset_tmp_grid3", "merge_test_mapset_tmp_grid4"],
  "outputs":[
    {"param": "raster", "value": "ndwi"},
    {"param": "vector", "value": "points,areas"},
    {"param": "strds", "value": "ndvi"}
  ],
  "keep_mapsets": "{{ keep_mapsets }}"
}"""


class PatchMergeTest(ActiniaResourceTestCaseBase):

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
    grids = ["grid1", "grid2", "grid3", "grid4"]
    created_mapsets = list()

    @classmethod
    def setUpClass(cls):
        super(PatchMergeTest, cls).setUpClass()
        accessible_datasets = {"nc_spm_08": ["PERMANENT"]}
        accessible_modules = ["t.create", "t.register"]
        cls.user_id, cls.user_group, cls.user_auth_header = cls.create_user(
            name="user", role="user", process_num_limit=30,
            process_time_limit=400, accessible_datasets=accessible_datasets,
            accessible_modules=accessible_modules)

    def _delete_mapset(self, mapset_name):
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

    def tearDown(self):
        for mapset in set(self.created_mapsets):
            self._delete_mapset(mapset)
        self.created_mapsets = list()
        self.app_context.pop()

    @pytest.mark.integrationtest
    def test_get_patch_apidocs(self):
        """Test the get method of merge patch endpoint"""
        # create mapset
        self.create_new_mapset(self.mapset, self.project)
        self.created_mapsets.append(self.mapset)

        url = f"{self.base_url}/merge_processes/patch"
        resp = self.server.get(url, headers=self.user_auth_header)

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

    def _create_grid(self):
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

    def _compute_in_tmp_mapsets(self):
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

    def _check_merge(self, keep_mapsets):
        # check mapsets
        mapset_url = (f"{URL_PREFIX}/{self.project_url_part}/{self.project}/"
                      "mapsets")
        rv_mapset = self.server.get(
            mapset_url,
            headers=self.user_auth_header,
        )
        resp_mapset = json_loads(rv_mapset.data)
        if keep_mapsets is True:
            for mapset in self.created_mapsets:
                assert mapset in resp_mapset["process_results"], \
                    f"Mapset '{mapset}' not in list."
        else:
            not_created_mapsets = list()
            for mapset in set(self.created_mapsets):
                if mapset == self.mapset:
                    assert mapset in resp_mapset["process_results"], \
                         f"Mapset '{mapset}' not in list."
                else:
                    assert mapset not in resp_mapset["process_results"], \
                         f"Mapset '{mapset}' in list."
                    not_created_mapsets.append(mapset)
            for mapset in not_created_mapsets:
                self.created_mapsets.remove(mapset)

        # check raster
        raster_url = f"{self.base_url}/raster_layers"
        rv_raster = self.server.get(
            raster_url,
            headers=self.user_auth_header,
        )
        resp_raster = json_loads(rv_raster.data)
        for rast in ["ndvi_1", "ndvi_2", "ndvi_3", "ndwi"]:
            assert rast in resp_raster["process_results"], \
                f"Raster '{rast}' not in list."

        # check vector
        vector_url = f"{self.base_url}/vector_layers"
        rv_vector = self.server.get(
            vector_url,
            headers=self.user_auth_header,
        )
        resp_vector = json_loads(rv_vector.data)
        for vect in ["areas", "points"]:
            assert vect in resp_vector["process_results"], \
                f"Vector '{vect}' not in list."

        # check strds
        strds_url = f"{self.base_url}/strds"
        rv_strds = self.server.get(
            strds_url,
            headers=self.user_auth_header,
        )
        resp_strds = json_loads(rv_strds.data)
        comp_strds = {
            "ndvi": [
                f"ndvi_1@{self.mapset}",
                f"ndvi_2@{self.mapset}",
                f"ndvi_3@{self.mapset}",
            ]
        }
        for strds in comp_strds:
            assert strds in resp_strds["process_results"], \
                f"STRDS '{strds}' not in list."
            strds2_url = f"{self.base_url}/strds/{strds}/raster_layers"
            rv2_strds = self.server.get(
                strds2_url,
                headers=self.user_auth_header,
            )
            resp_strds2 = json_loads(rv2_strds.data)
            strds_rast = [
                entry["id"] for entry in resp_strds2["process_results"]
            ]
            strds_rast.sort()
            assert strds_rast == comp_strds[strds], \
                f"Raster of STRDS '{strds}' are wrong."

    @pytest.mark.integrationtest
    def test_post_grid_keeping_mapsets(self):
        """Test the post method of tiling grid endpoint keeping the mapsets"""
        keep_mapsets = True

        # create mapset
        self.create_new_mapset(self.mapset, self.project)
        self.created_mapsets.append(self.mapset)

        self._create_grid()
        self._compute_in_tmp_mapsets()

        # merge
        url = f"{self.base_url}/merge_processes/patch"
        tpl = Template(PC_MERGE_PATCH)
        pc = tpl.render(keep_mapsets=str(keep_mapsets).lower())
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=pc,
        )
        self.waitAsyncStatusAssertHTTP(
            rv,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )

        self._check_merge(keep_mapsets)

    @pytest.mark.integrationtest
    def test_post_grid_deleting_mapsets(self):
        """Test the post method of tiling grid endpoint deleting the mapsets"""
        keep_mapsets = False

        # create mapset
        self.create_new_mapset(self.mapset, self.project)
        self.created_mapsets.append(self.mapset)

        self._create_grid()
        self._compute_in_tmp_mapsets()

        # merge
        url = f"{self.base_url}/merge_processes/patch"
        tpl = Template(PC_MERGE_PATCH)
        pc = tpl.render(keep_mapsets=str(keep_mapsets).lower())
        rv = self.server.post(
            url,
            headers=self.user_auth_header,
            content_type=self.content_type,
            data=pc,
        )
        self.waitAsyncStatusAssertHTTP(
            rv,
            headers=self.user_auth_header,
            http_status=200,
            status="finished",
        )
        self._check_merge(keep_mapsets)
