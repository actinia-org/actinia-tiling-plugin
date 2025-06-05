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

Add endpoints to flask app with endpoint definitions and routes
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

from flask_restful_swagger_2 import Resource

from actinia_tiling_plugin.api.tiling_list import TilingListResource
from actinia_tiling_plugin.api.tiling.tiling_grid import \
    AsyncTilingProcessGridResource
from actinia_tiling_plugin.api.merge_list import MergeListResource
from actinia_tiling_plugin.api.merge.patch_merge import \
    AsyncMergeProcessPatchResource


def get_endpoint_class_name(
    endpoint_class: Resource,
    projects_url_part: str = "projects",
) -> str:
    """Create the name for the given endpoint class."""
    endpoint_class_name = endpoint_class.__name__.lower()
    if projects_url_part != "projects":
        name = f"{endpoint_class_name}_{projects_url_part}"
    else:
        name = endpoint_class_name
    return name


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_project_endpoints(flask_api, projects_url_part="projects"):
    """
    Function to add resources with "projects" inside the endpoint url.
    Args:
        flask_api (flask_restful_swagger_2.Api): Flask api
        projects_url_part (str): The name of the projects inside the endpoint
                                 URL; to add deprecated location endpoints set
                                 it to "locations"
    """

    # tiling
    flask_api.add_resource(
        TilingListResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/tiling_processes",
        endpoint=get_endpoint_class_name(
            TilingListResource, projects_url_part
        ),
    )

    flask_api.add_resource(
        AsyncTilingProcessGridResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/tiling_processes/grid",
        endpoint=get_endpoint_class_name(
            AsyncTilingProcessGridResource, projects_url_part
        ),
    )

    # merge
    flask_api.add_resource(
        MergeListResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/merge_processes",
        endpoint=get_endpoint_class_name(
            MergeListResource, projects_url_part
        ),
    )
    flask_api.add_resource(
        AsyncMergeProcessPatchResource,
        f"/{projects_url_part}/<string:project_name>/mapsets/"
        "<string:mapset_name>/merge_processes/patch",
        endpoint=get_endpoint_class_name(
            AsyncMergeProcessPatchResource, projects_url_part
        ),
    )


def create_endpoints(flask_api):
    # add deprecated location and project endpoints
    create_project_endpoints(flask_api)
    create_project_endpoints(flask_api, projects_url_part="locations")
