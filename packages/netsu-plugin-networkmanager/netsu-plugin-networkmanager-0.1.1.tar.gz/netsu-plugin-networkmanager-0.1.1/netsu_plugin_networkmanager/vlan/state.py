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

from ..utils import nmcli
from ..utils_ip import parser as ip_parser

from . import VLAN_CONNECTION_PREFIX


def update(state):
    state['nm_vlan'] = get_vlans()


def get_vlans():
    vlans = {}

    connections = nmcli.list_connections()
    for connection in connections:
        if _is_vlan(connection):
            connection_info = nmcli.get_connection_info(connection['uuid'])
            name, attrs = _read_vlan_state(connection_info)
            vlans[name] = attrs

    return vlans


def _is_vlan(connection):
    return connection['name'].startswith(VLAN_CONNECTION_PREFIX)


def _read_vlan_state(connection_info):
    return connection_info['connection.interface-name'], {
        'ipv4': ip_parser.read_ipv4_state(connection_info)}
