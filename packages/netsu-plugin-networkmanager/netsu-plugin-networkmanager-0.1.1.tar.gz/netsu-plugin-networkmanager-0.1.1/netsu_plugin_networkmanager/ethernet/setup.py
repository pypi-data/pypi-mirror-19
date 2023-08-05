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

from . import ETHERNET_CONNECTION_PREFIX
from . import config


def detach_from_master(requested_config):
    system_ethernets = config.get_ethernets()
    requested_ethernets = requested_config['nm_ethernet']

    for ethernet, attrs in requested_ethernets.items():
        if ethernet in system_ethernets:
            system_attrs = system_ethernets[ethernet]
            if system_attrs['master'] != attrs['master']:
                connection_name = label.build_connection_name(
                    ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
                nmcli.run(['connection', 'modify', connection_name,
                           'connection.master', '',
                           'connection.slave-type', ''])


def remove(requested_config):
    system_ethernets = config.get_ethernets()
    requested_ethernets = requested_config['nm_ethernet']

    ethernets2remove = system_ethernets.keys() - requested_ethernets.keys()
    for ethernet in ethernets2remove:
        attrs = system_ethernets[ethernet]
        connection_name = label.build_connection_name(
            ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
        nmcli.run(['connection', 'delete', connection_name])


def add(requested_config):
    system_ethernets = config.get_ethernets()
    requested_ethernets = requested_config['nm_ethernet']

    ethernets2add = requested_ethernets.keys() - system_ethernets.keys()
    for ethernet in ethernets2add:
        attrs = requested_ethernets[ethernet]
        connection_name = label.build_connection_name(
            ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
        nmcli.run(['connection', 'add', 'type', 'ethernet',
                   'ifname', ethernet, 'con-name', connection_name,
                   'save', 'no', '--', 'ipv4.method', 'disabled'])


def attach_to_master(requested_config):
    system_ethernets = config.get_ethernets()
    requested_ethernets = requested_config['nm_ethernet']

    for ethernet, attrs in requested_ethernets.items():
        system_attrs = system_ethernets[ethernet]
        if system_attrs['master'] != attrs['master']:
            connection_name = label.build_connection_name(
                ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
            nmcli.run(['connection', 'modify', connection_name,
                       'connection.master', attrs['master']['name'],
                       'connection.slave-type', attrs['master']['type']])


def set_options(requested_config):
    system_ethernets = config.get_ethernets()
    requested_ethernets = requested_config['nm_ethernet']

    for ethernet, attrs in requested_ethernets.items():
        system_attrs = system_ethernets[ethernet]
        command = []
        if system_attrs['mtu'] != attrs['mtu']:
            command.extend(['ethernet.mtu',
                            str(attrs['mtu']) if attrs['mtu'] else '""'])
        if system_attrs['label'] != attrs['label']:
            new_connection_name = label.build_connection_name(
                ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
            command.extend(['connection.id', new_connection_name])
        command.extend(
            ip_setup.ipv4_changes(system_attrs['ipv4'], attrs['ipv4']))
        if command:
            connection_name = label.build_connection_name(
                ETHERNET_CONNECTION_PREFIX, system_attrs['label'], ethernet)
            nmcli.run(['connection', 'modify', connection_name] + command)


def turn_up(requested_config):
    requested_ethernets = requested_config['nm_ethernet']

    for ethernet, attrs in requested_ethernets.items():
        connection_name = label.build_connection_name(
            ETHERNET_CONNECTION_PREFIX, attrs['label'], ethernet)
        nmcli.run(['connection', 'up', connection_name])


def force_cleanup():
    connections = nmcli.list_connections()
    for connection in connections:
        if connection['name'].startswith(ETHERNET_CONNECTION_PREFIX):
            nmcli.run(['connection', 'delete', connection['uuid']])
