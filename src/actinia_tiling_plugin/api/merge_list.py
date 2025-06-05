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

Merge list class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

from copy import deepcopy
from flask import jsonify, make_response
from flask_restful_swagger_2 import swagger
from actinia_rest_lib.resource_base import ResourceBase

from actinia_tiling_plugin.apidocs import merge
from actinia_tiling_plugin.models.response_models.merge import \
    MergeListResponseModel


class MergeListResource(ResourceBase):
    """Returns a list of all merge processes"""

    @swagger.doc(merge.merge_list_get_docs)
    def get(self, project_name, mapset_name):
        """Returns a list of all merge processes"""

        patch_doc = merge.patch_merge_post_docs
        merge_docs = [("patch", patch_doc)]

        merge_processes = list()
        for (m_name, m_doc) in merge_docs:
            m_desc = dict()
            m_desc["categories"] = deepcopy(m_doc["tags"])
            m_desc["description"] = deepcopy(m_doc["description"])
            m_desc["id"] = deepcopy(m_name)
            merge_processes.append(m_desc)

        return make_response(jsonify(MergeListResponseModel(
            merge_processes=merge_processes), 200))
