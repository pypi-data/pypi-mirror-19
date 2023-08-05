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

from ..utils import label_definitions
from ..utils_ip import definitions as ip_definitions


ETHERNET = {
    'NMEthernetConfig': {
        'type': 'object',
        'default': {},
        'properties': {
            'ipv4': {
                '$ref': '#/definitions/NMIPv4Config'
            },
            'mtu': {
                'default': None,
                'anyOf': [
                    {'type': 'integer'},
                    {'type': 'null'}
                ]
            },
            'master': {
                'default': None,
                'anyOf': [
                    {
                        'type': 'object',
                        'required': ['name', 'type'],
                        'properties': {
                            'name': {
                                'type': 'string'
                            },
                            'type': {
                                'type': 'string'
                            }
                        }
                    },
                    {
                        'type': 'null'
                    }
                ]
            },
            'label': {
                '$ref': '#/definitions/NMLabel'
            }
        }
    }
}

ETHERNETS = {
    'NMEthernetsConfig': {
        'type': 'object',
        'default': {},
        'patternProperties': {
            '^[a-zA-Z0-9-]{1,16}$': {
                '$ref': '#/definitions/NMEthernetConfig'
            }
        },
        'additionalProperties': False
    }
}


def update(api_definitions):
    api_definitions.update(ip_definitions.IPv4_CONFIG)
    api_definitions.update(label_definitions.LABEL)
    api_definitions.update(ETHERNET)
    api_definitions.update(ETHERNETS)
    api_definitions['Config']['properties']['nm_ethernet'] = {
        '$ref': '#/definitions/NMEthernetsConfig'
    }
