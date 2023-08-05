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

from netsu_plugin_networkmanager.bond import config_definitions


definitions = {'Config': {'type': 'object', 'properties': {}}}
config_definitions.update(definitions)
schema = {'$ref': '#/definitions/Config', 'definitions': definitions}


@pytest.mark.unit
class TestValidBondData(object):

    def test_full_bond_definiton(self):
        DATA = {'nm_bond': {
            'bond1': {
                'mode': 'balance-rr',
                'primary': 'eth0',
                'miimon': 90,
                'ipv4': {
                    'mode': 'disabled'
                },
                'master': {'name': 'br0', 'type': 'bridge'},
                'label': 'green'}}}
        jsonschema.validate(DATA, schema)

    def test_empty_bond_definiton(self):
        DATA = {'nm_bond': {'bond1': {}}}
        jsonschema.validate(DATA, schema)

    def test_no_bond(self):
        DATA = {'nm_bond': {}}
        jsonschema.validate(DATA, schema)


@pytest.mark.unit
class TestInvalidBondData(object):

    def test_invalid_bond_name(self):
        DATA = {'nm_bond': {'longerthansixteenchars': {}}}
        print(schema)
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)

    def test_invalid_label(self):
        DATA = {'nm_bond': {'bond1': {'label': '! #'}}}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, schema)
