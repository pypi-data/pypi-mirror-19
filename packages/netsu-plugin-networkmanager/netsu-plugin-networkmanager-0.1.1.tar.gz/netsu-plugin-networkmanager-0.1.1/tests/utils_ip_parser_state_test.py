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
class TestState(object):

    def test_read_manual_ipv4_with_defined_gateway(self):
        IPv4_WITH_GATEWAY_CONNECTION = {
            'IP4.ADDRESSES': '192.168.100.2/24',
            'IP4.GATEWAY': '192.168.100.1'
        }
        IPv4_WITH_GATEWAY_STATE = {
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert (IPv4_WITH_GATEWAY_STATE ==
                parser.read_ipv4_state(IPv4_WITH_GATEWAY_CONNECTION))

    def test_read_manual_ipv4_without_defined_gateway(self):
        IPv4_WITHOUT_GATEWAY_CONNECTION = {
            'IP4.ADDRESSES': '192.168.100.2/24',
            'IP4.GATEWAY': ''
        }
        IPv4_WITHOUT_GATEWAY_STATE = {
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': None
        }
        assert (IPv4_WITHOUT_GATEWAY_STATE ==
                parser.read_ipv4_state(IPv4_WITHOUT_GATEWAY_CONNECTION))

    def test_read_auto_ipv4(self):
        IPv4_EMPTY_CONNECTION = {
            'IP4.ADDRESSES': '',
            'IP4.GATEWAY': ''
        }
        IPv4_EMPTY_STATE = {
            'addresses': [],
            'gateway': None
        }
        assert (IPv4_EMPTY_STATE ==
                parser.read_ipv4_state(IPv4_EMPTY_CONNECTION))
