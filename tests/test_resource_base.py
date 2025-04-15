#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016-2022 mundialis GmbH & Co. KG

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

Tests: Actinia resource test case base
"""

import atexit
import base64
import os
import signal
import time

from werkzeug.datastructures import Headers

from actinia_core.testsuite import ActiniaTestCaseBase, URL_PREFIX
from actinia_core.core.common.user import ActiniaUser
from actinia_core.core.common.config import global_config
from actinia_core.endpoints import create_endpoints


__license__ = "GPLv3"
__author__ = "Sören Gebbert, Anika Weinmann"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)
__maintainer__ = "mundialis GmbH & Co. KG"

# Create endpoints
create_endpoints()

kvdb_pid = None
server_test = False
custom_actinia_cfg = False

# If this environmental variable is set, then a real http request will be send
# instead of using the flask test_client.
if "ACTINIA_SERVER_TEST" in os.environ:
    server_test = bool(os.environ["ACTINIA_SERVER_TEST"])
# Set this variable to use a actinia config file in a docker container
if "ACTINIA_CUSTOM_TEST_CFG" in os.environ:
    custom_actinia_cfg = str(os.environ["ACTINIA_CUSTOM_TEST_CFG"])


def setup_environment():
    global kvdb_pid
    # Set the port to the test kvdb server
    global_config.KVDB_SERVER_SERVER = "localhost"
    global_config.KVDB_SERVER_PORT = 7000
    # Set the path to kvdb WORKER_LOGFILE
    # global_config.WORKER_LOGFILE = "/var/log/valkey/valkey"

    # home = os.getenv("HOME")

    # GRASS GIS
    # Setup the test environment
    global_config.GRASS_GIS_BASE = "/usr/local/grass/"
    global_config.GRASS_GIS_START_SCRIPT = "/usr/local/bin/grass"
    # global_config.GRASS_DATABASE= "/usr/local/grass_test_db"
    # global_config.GRASS_DATABASE = "%s/actinia/grass_test_db" % home
    global_config.GRASS_TMP_DATABASE = "/tmp"

    if server_test is False and custom_actinia_cfg is False:
        # Start the kvdb server for user and logging management
        kvdb_pid = os.spawnl(
            os.P_NOWAIT,
            "/usr/bin/valkey-server",
            "common/valkey.conf",
            "--port %i" % global_config.KVDB_SERVER_PORT,
        )
        time.sleep(1)

    if server_test is False and custom_actinia_cfg is not False:
        global_config.read(custom_actinia_cfg)


def stop_kvdb():
    if server_test is False:
        global kvdb_pid
        # Kill th kvdb server
        if kvdb_pid is not None:
            os.kill(kvdb_pid, signal.SIGTERM)


# Register the kvdb stop function
atexit.register(stop_kvdb)
# Setup the environment
setup_environment()


class ActiniaResourceTestCaseBase(ActiniaTestCaseBase):
    @classmethod
    def create_user(cls, name="guest", role="guest",
                    group="group", password="abcdefgh",
                    accessible_datasets=None, process_num_limit=1000,
                    process_time_limit=6000, accessible_modules=None):

        auth = bytes('%s:%s' % (name, password), "utf-8")

        # We need to create an HTML basic authorization header
        cls.auth_header[role] = Headers()
        cls.auth_header[role].add('Authorization',
                                  'Basic ' + base64.b64encode(auth).decode())

        # Make sure the user database is empty
        user = ActiniaUser(name)
        if user.exists():
            user.delete()
        # Create a user in the database
        user = ActiniaUser.create_user(name,
                                       group,
                                       password,
                                       user_role=role,
                                       accessible_datasets=accessible_datasets,
                                       process_num_limit=process_num_limit,
                                       process_time_limit=process_time_limit)
        if accessible_modules is None:
            accessible_modules = ["sleep"]
        user.add_accessible_modules(accessible_modules)
        user.update()
        cls.users_list.append(user)

        return name, group, cls.auth_header[role]
