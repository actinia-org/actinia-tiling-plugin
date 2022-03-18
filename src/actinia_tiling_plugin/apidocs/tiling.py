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


from actinia_tiling_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)


describeHelloWorld_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["example"],
    "description": "Hello World example",
    "responses": {
        "200": {
            "description": "This response returns the string 'Hello World!'",
            "schema": SimpleStatusCodeResponseModel,
        }
    },
}

grid_tiling_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["tiling"],
    "description": "Grid tiling",
    "responses": {
        "200": {
            "description": "",
            "schema": SimpleStatusCodeResponseModel,
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "detailed message",
                        "example": "Missing name in JSON content",
                    }
                },
            },
        },
    },
}
