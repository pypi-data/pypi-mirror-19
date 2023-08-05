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

import pytest

from netsu_plugin_networkmanager.utils_ip import parser


@pytest.mark.unit
class TestConfig(object):

    def test_read_manual_ipv4_with_defined_gateway(self):
        MANUAL_IPv4_WITH_GATEWAY_CONNECTION = {
            'ipv4.method': 'manual',
            'ipv4.addresses': '192.168.100.2/24',
            'ipv4.gateway': '192.168.100.1'
        }
        MANUAL_IPv4_WITH_GATEWAY_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert (MANUAL_IPv4_WITH_GATEWAY_CONFIG ==
                parser.read_ipv4_config(MANUAL_IPv4_WITH_GATEWAY_CONNECTION))

    def test_read_manual_ipv4_without_defined_gateway(self):
        MANUAL_IPv4_WITHOUT_GATEWAY_CONNECTION = {
            'ipv4.method': 'manual',
            'ipv4.addresses': '192.168.100.2/24',
            'ipv4.gateway': '--'
        }
        MANUAL_IPv4_WITHOUT_GATEWAY_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': None
        }
        assert (
            MANUAL_IPv4_WITHOUT_GATEWAY_CONFIG ==
            parser.read_ipv4_config(MANUAL_IPv4_WITHOUT_GATEWAY_CONNECTION))

    def test_read_auto_ipv4(self):
        AUTO_IPv4_CONNECTION = {
            'ipv4.method': 'auto',
            'ipv4.addresses': '',
            'ipv4.gateway': '--'
        }
        AUTO_IPv4_CONFIG = {
            'method': 'auto',
            'addresses': [],
            'gateway': None
        }
        assert (AUTO_IPv4_CONFIG ==
                parser.read_ipv4_config(AUTO_IPv4_CONNECTION))
