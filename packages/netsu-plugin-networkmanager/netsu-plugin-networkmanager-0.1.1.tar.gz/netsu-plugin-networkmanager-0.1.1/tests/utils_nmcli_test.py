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

from contextlib import contextmanager

import pytest

from netsu_plugin_networkmanager.utils import nmcli


BRIDGE_CONNECTION = 'con-test-br'
BRIDGE_DEVICE = 'test-br'


@contextmanager
def bridge(connection_name, interface_name):
    try:
        nmcli.run(['connection', 'add',
                   'con-name', connection_name, 'ifname', interface_name,
                   'save', 'no', 'type', 'bridge'])
        nmcli.run(['connection', 'up', connection_name])
        yield
    finally:
        nmcli.run(['connection', 'delete', BRIDGE_CONNECTION])


@pytest.mark.integration
class TestConnectionsGathering(object):

    def test_nmcli(self):
        with bridge(BRIDGE_CONNECTION, BRIDGE_DEVICE):
            pass

    def test_list_connections(self):
        with bridge(BRIDGE_CONNECTION, BRIDGE_DEVICE):
            connections = nmcli.list_connections()

        found = False
        for connection in connections:
            if connection['name'] == BRIDGE_CONNECTION:
                found = True
                assert isinstance(connection['uuid'], str)
                assert 'bridge' == connection['type']
                assert BRIDGE_DEVICE == connection['device']
        assert found

    def test_get_connection_info(self):
        with bridge(BRIDGE_CONNECTION, BRIDGE_DEVICE):
            connection_info = nmcli.get_connection_info(BRIDGE_CONNECTION)

        assert BRIDGE_CONNECTION == connection_info['connection.id']
