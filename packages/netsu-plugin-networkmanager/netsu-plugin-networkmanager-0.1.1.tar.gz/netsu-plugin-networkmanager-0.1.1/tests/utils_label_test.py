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

import pytest

from netsu_plugin_networkmanager.utils import label


@pytest.mark.unit
class TestLabelHandling(object):

    def test_get_label(self):
        LABEL = 'label'
        CONNECTION_NAME = 'prefix#label@device'
        assert LABEL == label.get_label(CONNECTION_NAME)

    def test_get_empty_label(self):
        CONNECTION_NAME = 'prefix@device'
        assert label.get_label(CONNECTION_NAME) is None

    def test_build_connection_name_with_label(self):
        PREFIX = 'prefix'
        LABEL = 'label'
        DEVICE = 'device'
        CONNECTION_NAME = 'prefix#label@device'
        assert (CONNECTION_NAME ==
                label.build_connection_name(PREFIX, LABEL, DEVICE))

    def test_build_connection_name_without_label(self):
        PREFIX = 'prefix'
        LABEL = None
        DEVICE = 'device'
        CONNECTION_NAME = 'prefix@device'
        assert (CONNECTION_NAME ==
                label.build_connection_name(PREFIX, LABEL, DEVICE))
