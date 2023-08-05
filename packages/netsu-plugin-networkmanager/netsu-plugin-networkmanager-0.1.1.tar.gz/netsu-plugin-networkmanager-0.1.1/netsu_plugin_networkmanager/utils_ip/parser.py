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


def read_ipv4_config(connection_info):
    method = connection_info.get('ipv4.method', 'disabled')

    raw_addresses = connection_info.get('ipv4.addresses', [])
    addresses = []
    if raw_addresses:
        for raw_address in raw_addresses.split(','):
            address, prefix = raw_address.split('/')
            addresses.append({'address': address, 'prefix': int(prefix)})

    raw_gateway = connection_info.get('ipv4.gateway')
    gateway = raw_gateway if raw_gateway != '--' else None

    return {'method': method,
            'addresses': addresses,
            'gateway': gateway}


def read_ipv4_state(connection_info):
    raw_addresses = [connection_info[key]
                     for key, value in connection_info.items()
                     if key.startswith('IP4.ADDRESS') and value]
    addresses = []
    for raw_address in raw_addresses:
        address, prefix = raw_address.split('/')
        addresses.append({'address': address, 'prefix': int(prefix)})

    raw_gateway = connection_info.get('IP4.GATEWAY')
    gateway = raw_gateway or None

    return {'addresses': addresses,
            'gateway': gateway}
