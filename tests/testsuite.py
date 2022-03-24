#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2021 mundialis GmbH & Co. KG
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
Test code for STAC module api endpoints
"""
__author__ = "Jorge Herrera"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"
__license__ = "GPLv3"


import base64
import unittest
from typing import Dict, List

import pwgen
from actinia_core.endpoints import create_endpoints
from actinia_core.core.common import redis_interface
from actinia_core.core.common.app import flask_app, URL_PREFIX
from actinia_core.core.common.config import global_config
from actinia_core.core.common.user import ActiniaUser
from flask.json import loads as json_loads
from time import sleep
from werkzeug.datastructures import Headers


# actinia-stac-plugin endpoints are included as defined in actinia_core
# config
create_endpoints()


class ActiniaTestCase(unittest.TestCase):

    user = None
    auth_header: Dict[str, Headers] = {}
    superadmin_auth_header: Dict[str, Headers] = {}
    users_list: List[str] = []

    @classmethod
    def setUpClass(cls):
        """Overwrites method setUp from unittest.TestCase class"""
        # Start and connect the redis interface
        redis_args = (global_config.REDIS_SERVER_URL, global_config.REDIS_SERVER_PORT)
        if global_config.REDIS_SERVER_PW and global_config.REDIS_SERVER_PW is not None:
            redis_args = (*redis_args, global_config.REDIS_SERVER_PW)
        redis_interface.connect(*redis_args)

        # create test user for roles user (more to come)
        accessible_datasets = {
            "nc_spm_08": [
                "PERMANENT", "user1", "modis_lst", "tiling_test_mapset"
            ]
        }
        password = pwgen.pwgen()
        cls.user_id, cls.user_group, cls.user_auth_header = cls.create_user(
            name="user",
            role="user",
            password=password,
            process_num_limit=3,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
        )
        cls.admin_id, cls.admin_group, cls.admin_auth_header = cls.create_user(
            name="admin", role="admin", accessible_datasets=accessible_datasets)

    @classmethod
    def tearDownClass(cls):
        """Overwrites method tearDown from unittest.TestCase class"""

        # remove test user; disconnect redis
        for user in cls.users_list:
            user.delete()
        redis_interface.disconnect()

    def setUp(self):
        # We need to set the application context
        self.app_context = flask_app.app_context()
        self.app_context.push()

        flask_app.testing = True
        self.app = flask_app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def create_new_mapset(self, mapset_name, location_name="nc_spm_08"):

        self.delete_mapset(mapset_name, location_name)
        # Create new mapset
        rv = self.app.post(
            URL_PREFIX + '/locations/%s/mapsets/%s' % (location_name, mapset_name),
            headers=self.admin_auth_header)
        print(rv.data.decode())

    def delete_mapset(self, mapset_name, location_name="nc_spm_08"):
        # Unlock mapset for deletion
        rv = self.app.delete(
            URL_PREFIX + '/locations/%s/mapsets/%s/lock' % (location_name, mapset_name),
            headers=self.admin_auth_header)
        print(rv.data.decode())
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)

        # Delete existing mapset
        rv2 = self.app.delete(
            URL_PREFIX + '/locations/%s/mapsets/%s' % (location_name, mapset_name),
            headers=self.admin_auth_header)
        print(rv2.data.decode())
        self.waitAsyncStatusAssertHTTP(rv2, headers=self.admin_auth_header)

    @classmethod
    def create_user(
        cls,
        name="guest",
        role="guest",
        group="group",
        password="abcdefgh",
        accessible_datasets=None,
        process_num_limit=1000,
        process_time_limit=6000,
    ):

        auth = bytes("%s:%s" % (name, password), "utf-8")

        # We need to create an HTML basic authorization header
        cls.auth_header[role] = Headers()
        cls.auth_header[role].add(
            "Authorization", "Basic " + base64.b64encode(auth).decode()
        )

        # Make sure the user database is empty
        user = ActiniaUser(name)
        if user.exists():
            user.delete()
        # Create a user in the database
        user = ActiniaUser.create_user(
            name,
            group,
            password,
            user_role=role,
            accessible_datasets=accessible_datasets,
            process_num_limit=process_num_limit,
            process_time_limit=process_time_limit,
        )
        user.add_accessible_modules(["uname", "sleep"])
        cls.users_list.append(user)

        return name, group, cls.auth_header[role]

    def waitAsyncStatusAssertHTTP(self, response, headers, http_status=200,
                                  status="finished", message_check=None):
        """Poll the status of a resource and assert its finished HTTP status
        The response will be checked if the resource was accepted. Hence it
        must always be HTTP 200 status.
        The status URL from the response is then polled until status: finished,
        error or terminated.
        The result of the poll can be checked against its HTTP status and its
        actinia status message.
        Args:
            response: The accept response
            http_status (int): The HTTP status that should be checked
            status (str): The return status of the response
            message_check (str): A string that must be in the message field
        Returns: response
        """
        # Check if the resource was accepted
        print("waitAsyncStatusAssertHTTP:", response.data.decode())
        self.assertEqual(response.status_code, 200,
                         "HTML status code is wrong %i" % response.status_code)
        self.assertEqual(response.mimetype, "application/json",
                         "Wrong mimetype %s" % response.mimetype)

        resp_data = json_loads(response.data)

        rv_user_id = resp_data["user_id"]
        rv_resource_id = resp_data["resource_id"]

        while True:
            rv = self.app.get(
                URL_PREFIX + "/resources/%s/%s" % (rv_user_id, rv_resource_id),
                headers=headers
            )
            print("waitAsyncStatusAssertHTTP in loop:", rv.data.decode())
            resp_data = json_loads(rv.data)
            if (resp_data["status"] == "finished"
                    or resp_data["status"] == "error"
                    or resp_data["status"] == "terminated"
                    or resp_data["status"] == "timeout"):
                break
            sleep(0.2)

        self.assertEqual(resp_data["status"], status)
        self.assertEqual(rv.status_code, http_status,
                         "HTML status code is wrong %i" % rv.status_code)

        if message_check is not None:
            self.assertTrue(message_check in resp_data["message"],
                            (f"Message is {resp_data['message']}"))

        sleep(0.4)
        return resp_data
