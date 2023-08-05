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


IP_ADDRESS_PATTERN = '^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$'


IPv4_CONFIG = {
    'NMIPv4Config': {
        'type': 'object',
        'default': {},
        'properties': {
            'method': {
                'type': 'string',
                'enum': ['auto', 'manual', 'disabled'],
                'default': 'disabled'
            },
            'addresses': {
                'type': 'array',
                'default': [],
                'items': {
                    'type': 'object',
                    'required': ['address', 'prefix'],
                    'properties': {
                        'address': {
                            'type': 'string',
                            'pattern': IP_ADDRESS_PATTERN
                        },
                        'prefix': {
                            'type': 'integer',
                            'minimum': 0,
                            'maximum': 32
                        }
                    }
                }
            },
            'gateway': {
                'default': None,
                'anyOf': [
                    {'type': 'string', 'pattern': IP_ADDRESS_PATTERN},
                    {'type': 'null'}
                ]
            }
        }
    }
}


IPv4_STATE = {
    'NMIPv4State': {
        'type': 'object',
        'properties': {
            'addresses': {
                'type': 'array',
                'default': [],
                'items': {
                    'type': 'object',
                    'properties': {
                        'address': {
                            'type': 'string',
                            'pattern': IP_ADDRESS_PATTERN
                        },
                        'prefix': {
                            'type': 'integer',
                            'minimum': 0,
                            'maximum': 32
                        }
                    }
                }
            },
            'gateway': {
                'anyOf': [
                    {'type': 'string', 'pattern': IP_ADDRESS_PATTERN},
                    {'type': 'null'}
                ]
            }
        }
    }
}
