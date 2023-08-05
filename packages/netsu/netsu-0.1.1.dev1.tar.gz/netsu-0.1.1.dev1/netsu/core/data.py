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

import json
import logging
import os

from . import errors
from . import utils


PERSISTENT_CONFIG = '/var/lib/netsu/persistent_config.json'
RUNNING_CONFIG = '/var/run/netsu_running_config.json'


class StoredData(object):
    def __init__(self, path):
        logging.info('Initializing {}'.format(self.__class__.__name__))
        self._path = path
        if not os.path.isfile(self._path):
            with utils.sync_open(self._path, 'w') as f:
                json.dump({}, f)

    def get(self):
        with utils.sync_open(self._path) as f:
            data = json.load(f)
        logging.debug('{} successfully loaded {}'.format(
            self.__class__.__name__, data))
        return data

    def set(self, data):
        logging.debug('{} is saving {}'.format(self.__class__.__name__, data))
        with utils.sync_open(self._path, 'w') as f:
            json.dump(data, f)


class PersistentConfig(StoredData):
    def __init__(self):
        super().__init__(PERSISTENT_CONFIG)


class RunningConfig(StoredData):
    def __init__(self, initial_data):
        super().__init__(RUNNING_CONFIG)
        self.set(initial_data)


class DataGatheringError(errors.NetsuCoreError):
    """An exception occurred while trying to gather report from plugins"""
    CODE = 21


class GatheredData(object):
    def __init__(self, update_functions):
        logging.info('Initializing {} with update functions {}'.format(
            self.__class__.__name__,
            ['{}:{}'.format(update.__module__, update.__name__)
             for update in update_functions]))
        self._update_functions = update_functions

    def get(self):
        data = {}
        for update in self._update_functions:
            try:
                update(data)
            except Exception as update_e:
                logging.exception(
                    'An exception occurred while updating {} with function '
                    '{}:{}'.format(data, update.__module__, update.__name__))
                raise DataGatheringError() from update_e
        logging.debug('{} successfully gathered data {}'.format(
            self.__class__.__name__, data))
        return data


class SystemConfig(GatheredData):
    def __init__(self, config_updates):
        super().__init__(config_updates)


class SystemState(GatheredData):
    def __init__(self, state_updates):
        super().__init__(state_updates)
