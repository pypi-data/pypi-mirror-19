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

from . import VLAN_CONNECTION_PREFIX
from . import config


def detach_from_master(requested_config):
    system_vlans = config.get_vlans()
    requested_vlans = requested_config['nm_vlan']

    for vlan, attrs in requested_vlans.items():
        if vlan in system_vlans:
            system_attrs = system_vlans[vlan]
            if system_attrs['master'] != attrs['master']:
                connection_name = label.build_connection_name(
                    VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
                nmcli.run(['connection', 'modify', connection_name,
                           'connection.master', '',
                           'connection.slave-type', ''])


def remove(requested_config):
    system_vlans = config.get_vlans()
    requested_vlans = requested_config['nm_vlan']

    vlans2remove = system_vlans.keys() - requested_vlans.keys()
    for vlan in vlans2remove:
        attrs = system_vlans[vlan]
        connection_name = label.build_connection_name(
            VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
        nmcli.run(['connection', 'delete', connection_name])


def add(requested_config):
    system_vlans = config.get_vlans()
    requested_vlans = requested_config['nm_vlan']

    vlans2add = requested_vlans.keys() - system_vlans.keys()
    for vlan in vlans2add:
        attrs = requested_vlans[vlan]
        connection_name = label.build_connection_name(
            VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
        nmcli.run(['connection', 'add', 'type', 'vlan',
                   'ifname', vlan, 'con-name', connection_name,
                   'dev', attrs['device'], 'id', str(attrs['id']),
                   'save', 'no', '--', 'ipv4.method', 'disabled'])


def attach_to_master(requested_config):
    system_vlans = config.get_vlans()
    requested_vlans = requested_config['nm_vlan']

    for vlan, attrs in requested_vlans.items():
        system_attrs = system_vlans[vlan]
        if system_attrs['master'] != attrs['master']:
            connection_name = label.build_connection_name(
                VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
            nmcli.run(['connection', 'modify', connection_name,
                       'connection.master', attrs['master']['name'],
                       'connection.slave-type', attrs['master']['type']])


def set_options(requested_config):
    system_vlans = config.get_vlans()
    requested_vlans = requested_config['nm_vlan']

    for vlan, attrs in requested_vlans.items():
        system_attrs = system_vlans[vlan]
        command = []
        if system_attrs['master'] != attrs['master']:
            command.extend(['vlan.master', attrs['master']])
        if system_attrs['id'] != attrs['id']:
            command.extend(['vlan.id', str(attrs['id'])])
        if system_attrs['label'] != attrs['label']:
            new_connection_name = label.build_connection_name(
                VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
            command.extend(['connection.id', new_connection_name])
        command.extend(
            ip_setup.ipv4_changes(system_attrs['ipv4'], attrs['ipv4']))
        if command:
            connection_name = label.build_connection_name(
                VLAN_CONNECTION_PREFIX, system_attrs['label'], vlan)
            nmcli.run(['connection', 'modify', connection_name] + command)


def turn_up(requested_config):
    requested_vlans = requested_config['nm_vlan']

    for vlan, attrs in requested_vlans.items():
        connection_name = label.build_connection_name(
            VLAN_CONNECTION_PREFIX, attrs['label'], vlan)
        nmcli.run(['connection', 'up', connection_name])


def force_cleanup():
    connections = nmcli.list_connections()
    for connection in connections:
        if connection['name'].startswith(VLAN_CONNECTION_PREFIX):
            nmcli.run(['connection', 'delete', connection['uuid']])
