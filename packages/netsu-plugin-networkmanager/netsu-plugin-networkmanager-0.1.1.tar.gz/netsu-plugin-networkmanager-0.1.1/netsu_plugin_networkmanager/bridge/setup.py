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

from . import BRIDGE_CONNECTION_PREFIX
from . import config


def remove(requested_config):
    system_bridges = config.get_bridges()
    requested_bridges = requested_config['nm_bridge']

    bridges2remove = system_bridges.keys() - requested_bridges.keys()
    for bridge in bridges2remove:
        attrs = system_bridges[bridge]
        connection_name = label.build_connection_name(
            BRIDGE_CONNECTION_PREFIX, attrs['label'], bridge)
        nmcli.run(['connection', 'delete', connection_name])


def add(requested_config):
    system_bridges = config.get_bridges()
    requested_bridges = requested_config['nm_bridge']

    bridges2add = requested_bridges.keys() - system_bridges.keys()
    for bridge in bridges2add:
        attrs = requested_bridges[bridge]
        connection_name = label.build_connection_name(
            BRIDGE_CONNECTION_PREFIX, attrs['label'], bridge)
        nmcli.run(['connection', 'add', 'type', 'bridge',
                   'ifname', bridge, 'con-name', connection_name,
                   'save', 'no', '--', 'ipv4.method', 'disabled'])


def set_options(requested_config):
    system_bridges = config.get_bridges()
    requested_bridges = requested_config['nm_bridge']

    for bridge, attrs in requested_bridges.items():
        system_attrs = system_bridges[bridge]
        command = []
        if system_attrs['stp'] != attrs['stp']:
            command.extend(['bridge.stp', 'yes' if attrs['stp'] else 'no'])
        if system_attrs['label'] != attrs['label']:
            new_connection_name = label.build_connection_name(
                BRIDGE_CONNECTION_PREFIX, attrs['label'], bridge)
            command.extend(['connection.id', new_connection_name])
        command.extend(
            ip_setup.ipv4_changes(system_attrs['ipv4'], attrs['ipv4']))
        if command:
            connection_name = label.build_connection_name(
                BRIDGE_CONNECTION_PREFIX, system_attrs['label'], bridge)
            nmcli.run(['connection', 'modify', connection_name] + command)


def turn_up(requested_config):
    requested_bridges = requested_config['nm_bridge']

    for bridge, attrs in requested_bridges.items():
        connection_name = label.build_connection_name(
            BRIDGE_CONNECTION_PREFIX, attrs['label'], bridge)
        nmcli.run(['connection', 'up', connection_name])


def force_cleanup():
    connections = nmcli.list_connections()
    for connection in connections:
        if connection['name'].startswith(BRIDGE_CONNECTION_PREFIX):
            nmcli.run(['connection', 'delete', connection['uuid']])
