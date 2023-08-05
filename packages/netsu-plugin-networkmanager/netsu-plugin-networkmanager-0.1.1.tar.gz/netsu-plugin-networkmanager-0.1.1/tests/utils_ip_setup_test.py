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

from netsu_plugin_networkmanager.utils_ip import setup


@pytest.mark.unit
class TestSetup(object):

    def test_no_needed_changes(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        REQUESTED_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert [] == setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG)

    def test_change_method_from_manual_to_auto(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        REQUESTED_CONFIG = {
            'method': 'auto',
            'addresses': [],
            'gateway': None
        }
        assert (['ipv4.method', 'auto',
                 'ipv4.addresses', '',
                 'ipv4.gateway', ''] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))

    def test_change_method_from_auto_to_manual(self):
        SYSTEM_CONFIG = {
            'method': 'auto',
            'addresses': [],
            'gateway': None
        }
        REQUESTED_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert (['ipv4.method', 'manual',
                 'ipv4.addresses', '192.168.100.2/24',
                 'ipv4.gateway', '192.168.100.1'] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))

    def test_change_method_from_manual_to_disabled(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        REQUESTED_CONFIG = {
            'method': 'disabled',
            'addresses': [],
            'gateway': None
        }
        assert (['ipv4.method', 'disabled',
                 'ipv4.addresses', '',
                 'ipv4.gateway', ''] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))

    def test_add_gateway(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': None
        }
        REQUESTED_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert (['ipv4.gateway', '192.168.100.1'] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))

    def test_remove_gateway(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        REQUESTED_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': None
        }
        assert (['ipv4.gateway', ''] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))

    def test_set_multiple_addresses(self):
        SYSTEM_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        REQUESTED_CONFIG = {
            'method': 'manual',
            'addresses': [{'address': '192.168.100.2', 'prefix': 24},
                          {'address': '192.168.100.3', 'prefix': 24}],
            'gateway': '192.168.100.1'
        }
        assert (['ipv4.addresses', '192.168.100.2/24,192.168.100.3/24'] ==
                setup.ipv4_changes(SYSTEM_CONFIG, REQUESTED_CONFIG))
