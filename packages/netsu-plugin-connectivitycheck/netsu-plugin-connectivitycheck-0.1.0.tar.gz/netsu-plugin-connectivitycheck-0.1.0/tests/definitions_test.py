# Copyright (C) 2016 Petr Horacek <phoracek@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import jsonschema
import pytest

from netsu_plugin_connectivitycheck import definitions


_definitions = {'Parameters': {'type': 'object', 'properties': {}}}
definitions.update(_definitions)
schema = {'$ref': '#/definitions/Parameters', 'definitions': _definitions}


@pytest.mark.unit
class TestValidParameters(object):

    def test_address(self):
        DATA = {'connectivitycheck_ping': {'address': 'www.example.org',
                                           'timeout': 10}}
        jsonschema.validate(DATA, schema)

    def test_ipv4_address(self):
        DATA = {'connectivitycheck_ping': {'address': '127.0.0.1'}}
        jsonschema.validate(DATA, schema)

    def test_ipv6_address(self):
        DATA = {'connectivitycheck_ping': {'address': '::1'}}
        jsonschema.validate(DATA, schema)

    def test_check_disabled(self):
        DATA = {}
        jsonschema.validate(DATA, schema)
