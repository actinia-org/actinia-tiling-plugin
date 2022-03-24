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

Hello World class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from actinia_core.models.response_models import (
    ProcessingErrorResponseModel,
)

from actinia_tiling_plugin.models.response_models import (
    SimpleStatusCodeResponseModel,
    GridTilingResponseModel,
    TilingListResponseModel,
)


tiling_list_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Tiling"],
    "description": "Returns The list of the tiling processes.",
    "responses": {
        "200": {
            "description": "This response returns list of the tiling "
            "processes.",
            "schema": TilingListResponseModel,
        }
    },
}

grid_tiling_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Tiling"],
    "description": "Returns only the api description of the POST endpoint.",
    "responses": {
        "200": {
            "description": "This response returns the api description of the "
                           "POST endpoint.",
            "schema": SimpleStatusCodeResponseModel,
        }
    },
}

# class
grid_tiling_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["Tiling"],
    "description": "Creates grid tiles with a speciefied 'width' and 'height' "
                   "in the current computational region. The created grids "
                   "have the given 'grid_prefix' and will be listed in the "
                   "'process_results'. "
                   "Minimum required user role: user.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "width",
            "description": "The width of one grid tile in map units.",
            "required": True,
            "in": "body",
            "schema": {"type": "string"}
        },
        {
            "name": "height",
            "description": "The height of one grid tile in map units.",
            "required": True,
            "in": "body",
            "schema": {"type": "string"}
        },
        {
            "name": "grid_prefix",
            "description": "The prefix of the grid tiles.",
            "required": True,
            "in": "body",
            "schema": {"type": "string"}
        }
    ],
    "responses": {
        "200": {
            "description": "This response returns the processing response with"
                           " the grid tile names in the 'processing_results'.",
            "schema": GridTilingResponseModel
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": ProcessingErrorResponseModel
        },
    },
}
