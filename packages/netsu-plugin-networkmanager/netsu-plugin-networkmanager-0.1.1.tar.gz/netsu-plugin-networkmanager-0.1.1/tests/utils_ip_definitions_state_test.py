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


IPv4_STATE_SCHEMA = definitions.IPv4_STATE['NMIPv4State']


@pytest.mark.unit
class TestValidIPv4Data(object):

    def test_with_gateway(self):
        DATA = {
            'addresses': [
                {'address': '192.168.0.2', 'prefix': 24},
                {'address': '192.168.0.3', 'prefix': 24}],
            'gateway': '192.168.0.1'}
        jsonschema.validate(DATA, IPv4_STATE_SCHEMA)

    def test_without_gateway(self):
        DATA = {
            'addresses': [
                {'address': '192.168.0.2', 'prefix': 24},
                {'address': '192.168.0.3', 'prefix': 24}],
            'gateway': None}
        jsonschema.validate(DATA, IPv4_STATE_SCHEMA)

    def test_without_addresses(self):
        DATA = {'addresses': [],
                'gateway': None}
        jsonschema.validate(DATA, IPv4_STATE_SCHEMA)
