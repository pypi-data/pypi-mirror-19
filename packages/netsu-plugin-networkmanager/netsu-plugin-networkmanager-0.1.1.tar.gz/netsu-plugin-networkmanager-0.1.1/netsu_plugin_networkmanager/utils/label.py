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


def build_connection_name(prefix, label, device):
    if label:
        return '{}#{}@{}'.format(prefix, label, device)
    else:
        return '{}@{}'.format(prefix, device)


def get_label(connection_name):
    label_start = connection_name.find('#')
    if label_start >= 0:
        label_stop = connection_name.index('@')
        return connection_name[label_start + 1:label_stop]
    else:
        return None
