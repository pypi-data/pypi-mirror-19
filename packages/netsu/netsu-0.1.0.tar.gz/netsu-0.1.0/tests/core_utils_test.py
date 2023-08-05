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

from threading import Thread
from time import sleep
import os

import pytest

from netsu.core import utils


@pytest.mark.unit
class TestSyncOpen(object):

    def test_open_write_read(self, tmpdir):
        TEXT = 'shruberry'
        path = str(tmpdir.join('testfile'))

        with utils.sync_open(path, 'a') as f:
            f.write(TEXT)
        with utils.sync_open(path) as f:
            assert TEXT == f.read()

    def test_sychronous_access(self, tmpdir):
        SLEEP = 0.1
        path = str(tmpdir.join('testfile'))

        def open_and_sleep():
            with utils.sync_open(path, 'a'):
                sleep(SLEEP)

        thread_a = Thread(target=open_and_sleep)
        thread_b = Thread(target=open_and_sleep)
        time_start = os.times()[4]
        thread_a.start()
        thread_b.start()
        thread_a.join()
        thread_b.join()
        time_stop = os.times()[4]

        assert time_stop - time_start > 1.9 * SLEEP
