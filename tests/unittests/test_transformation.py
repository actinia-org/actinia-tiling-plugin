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

First test
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"

import pytest
from actinia_tiling_plugin.core.example import transform_input


@pytest.mark.unittest
@pytest.mark.parametrize(
    "inp,ref_out",
    [("test", "Hello world TEST!"), ("bla23", "Hello world BLA23!")],
)
def test_transform_input(inp, ref_out):
    """Test for tranform_input function."""
    out = transform_input(inp)
    assert out == ref_out, f"Wrong result from transform_input for {inp}"
