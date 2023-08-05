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


def update_a(config):
    config['a'] = 1
    config['b'] = {}


def update_b(config):
    config['a'] = 2
    config['b']['c'] = 3


def update_c(config):
    config['b']['d'] = 4


def update_d(config):
    raise Exception()


@pytest.mark.unit
class TestGatheredData(object):

    def test_update(self):
        SORTED_UPDATE_FUNCTIONS = [update_a, update_b, update_c]
        EXPECTED_GATHERED_REPORT = {'a': 2, 'b': {'c': 3, 'd': 4}}
        data_gatherer = data.GatheredData(SORTED_UPDATE_FUNCTIONS)
        assert EXPECTED_GATHERED_REPORT == data_gatherer.get()

    def test_gathering_error(self):
        SORTED_UPDATE_FUNCTIONS = [update_a, update_d]
        data_gatherer = data.GatheredData(SORTED_UPDATE_FUNCTIONS)
        with pytest.raises(data.DataGatheringError):
            data_gatherer.get()
