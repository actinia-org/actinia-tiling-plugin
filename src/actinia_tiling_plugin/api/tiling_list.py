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

Tiling list class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

from copy import deepcopy
from flask import jsonify, make_response
from flask_restful_swagger_2 import swagger
from actinia_rest_lib.resource_base import ResourceBase

from actinia_tiling_plugin.apidocs import tiling
from actinia_tiling_plugin.models.response_models.tiling import \
    TilingListResponseModel


class TilingListResource(ResourceBase):
    """Returns a list of all tiling prcesses"""

    @swagger.doc(tiling.tiling_list_get_docs)
    def get(self, project_name, mapset_name):
        """Returns a list of all tiling prcesses"""

        grid_doc = tiling.grid_tiling_post_docs
        tiling_docs = [("grid", grid_doc)]

        tiling_processes = list()
        for (t_name, t_doc) in tiling_docs:
            t_desc = dict()
            t_desc["categories"] = deepcopy(t_doc["tags"])
            t_desc["description"] = deepcopy(t_doc["description"])
            t_desc["id"] = deepcopy(t_name)
            tiling_processes.append(t_desc)

        return make_response(jsonify(TilingListResponseModel(
            tiling_processes=tiling_processes), 200))
