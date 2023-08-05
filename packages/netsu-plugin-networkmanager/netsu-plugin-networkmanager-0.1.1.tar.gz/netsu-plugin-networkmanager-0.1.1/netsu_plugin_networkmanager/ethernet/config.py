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

from ..utils import label
from ..utils import nmcli
from ..utils_ip import parser as ip_parser

from . import ETHERNET_CONNECTION_PREFIX


def update(config):
    config['nm_ethernet'] = get_ethernets(only_active=True)


def get_ethernets(only_active=False):
    ethernets = {}

    connections = nmcli.list_connections()
    for connection in connections:
        if only_active and not _is_active(connection):
            continue
        if _is_ethernet(connection):
            connection_info = nmcli.get_connection_info(connection['uuid'])
            name, attrs = _read_ethernet_config(connection_info)
            ethernets[name] = attrs

    return ethernets


def _is_active(connection):
    return connection['device'] is not None


def _is_ethernet(connection):
    return connection['name'].startswith(ETHERNET_CONNECTION_PREFIX)


def _read_master(connection_info):
    master = connection_info['connection.master']
    slave_type = connection_info['connection.slave-type']
    return {'name': master, 'type': slave_type} if master != '--' else None


def _read_ethernet_config(connection_info):
    return connection_info['connection.interface-name'], {
        'ipv4': ip_parser.read_ipv4_config(connection_info),
        'mtu': (None if connection_info['802-3-ethernet.mtu'] == 'auto'
                else int(connection_info['802-3-ethernet.mtu'])),
        'master': _read_master(connection_info),
        'label': label.get_label(connection_info['connection.id'])}
