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

from netsu_plugin_networkmanager.utils_ip import definitions


IPv4_CONFIG_SCHEMA = definitions.IPv4_CONFIG['NMIPv4Config']


@pytest.mark.unit
class TestValidIPv4Data(object):

    def test_manual_all_provided(self):
        DATA = {'method': 'manual',
                'addresses': [
                    {'address': '192.168.0.2', 'prefix': 24},
                    {'address': '192.168.0.3', 'prefix': 24}],
                'gateway': '192.168.0.1'}
        jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_auto(self):
        DATA = {'method': 'auto'}
        jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_auto_with_defaults_prefilled(self):
        DATA = {'method': 'auto',
                'addresses': [],
                'gateway': None}
        jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)


@pytest.mark.unit
class TestInvalidIPv4Data(object):

    def test_invalid_method(self):
        DATA = {'method': 'shruberry'}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_address_out_of_range(self):
        DATA = {'method': 'manual',
                'addresses': [{'address': '300.168.0.2', 'prefix': 24}]}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_invalid_address_format(self):
        DATA = {'method': 'manual',
                'addresses': [{'address': 'not-an-address', 'prefix': 24}]}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_address_with_missing_prefix(self):
        DATA = {'method': 'manual',
                'addresses': [{'address': '192.168.0.2'}]}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)

    def test_invalid_prefix(self):
        DATA = {'method': 'manual',
                'addresses': [{'address': 'not-an-address', 'prefix': 33}]}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(DATA, IPv4_CONFIG_SCHEMA)
