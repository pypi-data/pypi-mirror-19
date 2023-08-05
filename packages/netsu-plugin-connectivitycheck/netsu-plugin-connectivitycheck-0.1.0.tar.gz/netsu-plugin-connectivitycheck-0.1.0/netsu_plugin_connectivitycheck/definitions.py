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


PING_CHECK = {
    'ConnectivityCheckPing': {
        'type': 'object',
        'required': ['address'],
        'properties': {
            'address': {'type': 'string'},
            'timeout': {'type': 'integer', 'default': 10}
        }
    }
}


def update(api_definitions):
    api_definitions.update(PING_CHECK)
    parameters_properties = api_definitions['Parameters']['properties']
    parameters_properties['connectivitycheck_ping'] = {
        '$ref': '#/definitions/ConnectivityCheckPing'
    }
