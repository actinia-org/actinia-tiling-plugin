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

Functions for the processing
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

import json

from actinia_core.core.common.process_chain import ProcessChainConverter

from actinia_tiling_plugin.resources.templating import tplEnv


pconv = ProcessChainConverter()


def pctpl_to_pl(tpl_file, tpl_values):
    tpl = tplEnv.get_template(tpl_file)
    pc = json.loads(
        tpl.render(**tpl_values).replace('\n', '').replace(" ", ""))
    pl = pconv.process_chain_to_process_list(pc)
    return pl, pconv
