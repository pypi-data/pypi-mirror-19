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

from netsu.core import data


@pytest.mark.unit
class TestStoredData(object):
    STORAGE_NAME = 'data.json'

    def test_initialize_without_existing_storage(self, tmpdir):
        path = tmpdir.join(self.STORAGE_NAME)

        stored_data = data.StoredData(str(path))

        assert {} == stored_data.get()
        assert path.exists()

    def test_initialize_with_already_existing_storage(self, tmpdir):
        DATA = {'a': 1}
        path = tmpdir.join(self.STORAGE_NAME)

        stored_data = data.StoredData(str(path))
        stored_data.set(DATA)
        another_stored_data = data.StoredData(str(path))

        assert DATA == another_stored_data.get()
