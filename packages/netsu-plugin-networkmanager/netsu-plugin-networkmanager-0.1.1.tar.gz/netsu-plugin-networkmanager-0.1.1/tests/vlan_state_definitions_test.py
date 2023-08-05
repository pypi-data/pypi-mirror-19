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

from netsu_plugin_networkmanager.vlan import state_definitions


definitions = {'State': {'type': 'object', 'properties': {}}}
state_definitions.update(definitions)
schema = {'$ref': '#/definitions/State', 'definitions': definitions}


@pytest.mark.unit
class TestValidVlanData(object):

    def test_full_vlan_state_description(self):
        DATA = {'nm_vlan': {
            'vlan1': {
                'ipv4': {
                    'mode': 'disabled',
                    'addresses': [],
                    'gateway': None
                }}}}
        jsonschema.validate(DATA, schema)


@pytest.mark.unit
class TestInvalidVlanData(object):

    def test_invalid_vlan_name(self):
        DATA = {'nm_vlan': {'longerthansixteenchars': {}}}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)
