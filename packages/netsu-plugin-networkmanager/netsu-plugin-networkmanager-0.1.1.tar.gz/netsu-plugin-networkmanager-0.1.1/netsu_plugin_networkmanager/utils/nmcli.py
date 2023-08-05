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

import subprocess


_NMCLI = '/usr/bin/nmcli'


class NmcliError(Exception):
    pass


def list_connections():
    connections_lines = run([
        '--terse',
        '--fields', 'NAME,UUID,TYPE,DEVICE',
        'connection', 'show'])
    connections = []
    for line in connections_lines:
        name, uuid, con_type, device = line.strip().split(':')
        connections.append({
            'name': name,
            'uuid': uuid,
            'type': con_type,
            'device': device if device != '--' else None})
    return connections


def get_connection_info(identificator):
    connection_lines = run([
        '--terse',
        'connection', 'show', identificator])
    info = {}
    for line in connection_lines:
        split = line.split(':', 1)
        if len(split) == 2:
            key, value = split
        else:
            key, value = split[0], ''
        info[key] = value
    return info


def run(command):
    try:
        lines = subprocess.check_output([_NMCLI] + command,
                                        universal_newlines=True,
                                        stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise NmcliError(e.returncode, e.output)
    return lines.strip().split('\n')
