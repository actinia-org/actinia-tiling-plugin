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

Merge apidocs
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from actinia_core.models.response_models import (
    ProcessingErrorResponseModel,
    ProcessingResponseModel,
)
from actinia_core.models.process_chain import IOParameterBase

from actinia_tiling_plugin.models.response_models.general import (
    SimpleStatusCodeResponseModel,
)
from actinia_tiling_plugin.models.response_models.merge import (
    MergeListResponseModel,
)


merge_list_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Merge"],
    "description": "Returns The list of the merge processes.",
    "responses": {
        "200": {
            "description": "This response returns list of the merge "
            "processes.",
            "schema": MergeListResponseModel,
        }
    },
}

patch_merge_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Merge"],
    "description": "Returns only the API description of the POST endpoint.",
    "responses": {
        "200": {
            "description": "This response returns the API description of the "
                           "POST endpoint.",
            "schema": SimpleStatusCodeResponseModel,
        }
    },
}

patch_merge_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Merge"],
    "description": "Merge raster, vector and STRDS data from different "
    "mapsets defined in a 'mapsetlist' by patching them "
    "in the new/target mapset. Minimum required user role: user.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "mapsetlist",
            "description": "The list of mapset names which should be merged "
            "into the given mapset.",
            "required": True,
            "in": "body",
            "schema": {"type": "string"}
        },
        {
            "name": "outputs",
            "description": "A list of output parameters.",
            "required": True,
            "in": "body",
            "schema": IOParameterBase
        },
        {
            "name": "keep_mapsets",
            "description": "A boolean if it is set to 'true' then the merged "
            "mapsets will not be deleted. The default falue is 'false', so "
            "the merged mapset will be deleted.",
            "required": False,
            "in": "body",
            "schema": {"type": "bool"}
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns the processing response.",
            "schema": ProcessingResponseModel
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": ProcessingErrorResponseModel
        },
    },
}
