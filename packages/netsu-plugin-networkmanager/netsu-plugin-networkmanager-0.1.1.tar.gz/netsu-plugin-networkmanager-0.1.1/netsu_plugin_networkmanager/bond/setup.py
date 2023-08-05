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
from ..utils import label
from ..utils_ip import setup as ip_setup

from . import BOND_CONNECTION_PREFIX
from . import config


def detach_from_master(requested_config):
    system_bonds = config.get_bonds()
    requested_bonds = requested_config['nm_bond']

    for bond, attrs in requested_bonds.items():
        if bond in system_bonds:
            system_attrs = system_bonds[bond]
            if system_attrs['master'] != attrs['master']:
                connection_name = label.build_connection_name(
                    BOND_CONNECTION_PREFIX, attrs['label'], bond)
                nmcli.run(['connection', 'modify', connection_name,
                           'connection.master', '',
                           'connection.slave-type', ''])


def remove(requested_config):
    system_bonds = config.get_bonds()
    requested_bonds = requested_config['nm_bond']

    bonds2remove = system_bonds.keys() - requested_bonds.keys()
    for bond in bonds2remove:
        attrs = system_bonds[bond]
        connection_name = label.build_connection_name(
            BOND_CONNECTION_PREFIX, attrs['label'], bond)
        nmcli.run(['connection', 'delete', connection_name])


def add(requested_config):
    system_bonds = config.get_bonds()
    requested_bonds = requested_config['nm_bond']

    bonds2add = requested_bonds.keys() - system_bonds.keys()
    for bond in bonds2add:
        attrs = requested_bonds[bond]
        connection_name = label.build_connection_name(
            BOND_CONNECTION_PREFIX, attrs['label'], bond)
        nmcli.run(['connection', 'add', 'type', 'bond',
                   'ifname', bond, 'con-name', connection_name,
                   'save', 'no', '--', 'ipv4.method', 'disabled'])


def attach_to_master(requested_config):
    system_bonds = config.get_bonds()
    requested_bonds = requested_config['nm_bond']

    for bond, attrs in requested_bonds.items():
        system_attrs = system_bonds[bond]
        if system_attrs['master'] != attrs['master']:
            connection_name = label.build_connection_name(
                BOND_CONNECTION_PREFIX, attrs['label'], bond)
            nmcli.run(['connection', 'modify', connection_name,
                       'connection.master', attrs['master']['name'],
                       'connection.slave-type', attrs['master']['type']])


def set_options(requested_config):
    system_bonds = config.get_bonds()
    requested_bonds = requested_config['nm_bond']

    for bond, attrs in requested_bonds.items():
        system_attrs = system_bonds[bond]
        command = []

        bond_options = {}
        bond_options['mode'] = attrs['mode']
        bond_options['miimon'] = attrs['miimon']
        primary = attrs.get('primary')
        if primary:
            bond_options['primary'] = attrs['primary']
        command.extend(
            ['bond.options',
             (','.join('{}={}'.format(key, value) for
              key, value in bond_options.items()))])

        if system_attrs['label'] != attrs['label']:
            new_connection_name = label.build_connection_name(
                BOND_CONNECTION_PREFIX, attrs['label'], bond)
            command.extend(['connection.id', new_connection_name])
        command.extend(
            ip_setup.ipv4_changes(system_attrs['ipv4'], attrs['ipv4']))

        connection_name = label.build_connection_name(
            BOND_CONNECTION_PREFIX, system_attrs['label'], bond)
        nmcli.run(['connection', 'modify', connection_name] + command)


def turn_up(requested_config):
    requested_bonds = requested_config['nm_bond']

    for bond, attrs in requested_bonds.items():
        connection_name = label.build_connection_name(
            BOND_CONNECTION_PREFIX, attrs['label'], bond)
        nmcli.run(['connection', 'up', connection_name])


def force_cleanup():
    connections = nmcli.list_connections()
    for connection in connections:
        if connection['name'].startswith(BOND_CONNECTION_PREFIX):
            nmcli.run(['connection', 'delete', connection['uuid']])
