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

import jsonschema
import pytest

from netsu_plugin_networkmanager.utils import label_definitions


@pytest.mark.unit
class TestLabelDefinition(object):

    def test_valid_label(self):
        LABEL = 'foo_bar-baz'
        jsonschema.validate(LABEL, label_definitions.LABEL['NMLabel'])

    def test_valid_none_label(self):
        LABEL = None
        jsonschema.validate(LABEL, label_definitions.LABEL['NMLabel'])

    def test_invalid_label(self):
        LABEL = 'foo$bar*baz'
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(LABEL, label_definitions.LABEL['NMLabel'])
