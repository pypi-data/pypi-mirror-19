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

from . import BOND_CONNECTION_PREFIX


def update(config):
    config['nm_bond'] = get_bonds(only_active=True)


def get_bonds(only_active=False):
    bonds = {}

    connections = nmcli.list_connections()
    for connection in connections:
        if only_active and not _is_active(connection):
            continue
        if _is_bond(connection):
            connection_info = nmcli.get_connection_info(connection['uuid'])
            name, attrs = _read_bond_config(connection_info)
            bonds[name] = attrs

    return bonds


def _is_active(connection):
    return connection['device'] is not None


def _is_bond(connection):
    return connection['name'].startswith(BOND_CONNECTION_PREFIX)


def _read_master(connection_info):
    master = connection_info['connection.master']
    slave_type = connection_info['connection.slave-type']
    return {'name': master, 'type': slave_type} if master != '--' else None


def _read_bond_config(connection_info):
    bond_options = dict(
        key_value.split('=', 1)
        for key_value in connection_info['bond.options'].split(','))
    return connection_info['connection.interface-name'], {
        'mode': bond_options.get('mode', 'balance-rr'),
        'primary': bond_options.get('primary'),
        'miimon': int(bond_options.get('miimon', 100)),
        'ipv4': ip_parser.read_ipv4_config(connection_info),
        'master': _read_master(connection_info),
        'label': label.get_label(connection_info['connection.id'])}
