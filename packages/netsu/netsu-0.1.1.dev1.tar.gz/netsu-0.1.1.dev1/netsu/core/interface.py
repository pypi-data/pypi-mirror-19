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

import logging
import os

from . import configurator
from . import data
from . import plugins
from . import utils
from . import validation


VALIDATE_OUTPUT_ENV_VARIABLE = 'NETSU_VALIDATE_OUTPUT'

SET_RUNNING_CONFIG_LOCK_PATH = '/var/run/netsu_set_running_config.lock'


class Interface(object):

    def __init__(self):
        self._debug_mode = _debug_mode()
        logging.info('Interface output validation is {}'.format(
            'enabled' if self._debug_mode else 'disabled'))

        definitions = _build_definitions()
        self._parameters_validator = validation.Validator(
            _build_parameters_schema(definitions))
        self._config_validator = validation.Validator(
            _build_config_schema(definitions))
        if self._debug_mode:
            self._state_validator = validation.Validator(
                _build_state_schema(definitions))

        # use validation to fill in empty defaults
        initial_running_config = {}
        self._config_validator.validate_and_set_defaults(
            initial_running_config)
        self._running_config = data.RunningConfig(initial_running_config)

        self._persistent_config = data.PersistentConfig()

        self._system_config = data.SystemConfig(plugins.get_config_updates())
        self._system_state = data.SystemState(plugins.get_state_updates())

        self._configurator = configurator.Configurator(
            plugins.get_setup_steps(), plugins.get_force_cleanup_steps(),
            self._running_config, self._system_config)

    def get_persistent_config(self):
        return self._get_config(self._persistent_config)

    def set_persistent_config(self, config):
        self._config_validator.validate_and_set_defaults(config)
        self._persistent_config.set(config)

    def get_running_config(self):
        return self._get_config(self._running_config)

    def set_running_config(self, config, parameters):
        self._config_validator.validate_and_set_defaults(config)
        self._parameters_validator.validate_and_set_defaults(parameters)
        with utils.sync_open(SET_RUNNING_CONFIG_LOCK_PATH, 'a'):
            try:
                self._configurator.run(config, parameters)
                self._running_config.set(config)
            except (configurator.CriticalSetupError,
                    configurator.FatalSetupError):
                self._running_config.set({})
                raise

    def get_system_config(self):
        return self._get_config(self._system_config)

    def get_system_state(self):
        return self._get_state(self._system_state)

    def _get_config(self, config_class):
        config = config_class.get()
        if self._debug_mode:
            self._config_validator.validate(config)
        return config

    def _get_state(self, state_class):
        state = self._system_state.get()
        if self._debug_mode:
            self._state_validator.validate(state)
        return state


def _debug_mode():
    return bool(int(os.environ.get(VALIDATE_OUTPUT_ENV_VARIABLE, '0')))


def _build_definitions():
    definitions = {
        'Parameters': {'type': 'object', 'properties': {}},
        'Config': {'type': 'object', 'properties': {}},
        'State': {'type': 'object', 'properties': {}}}
    for update in plugins.get_definitions_updates():
        update(definitions)
    return definitions


def _build_parameters_schema(definitions):
    return {'$ref': '#/definitions/Parameters', 'definitions': definitions}


def _build_config_schema(definitions):
    return {'$ref': '#/definitions/Config', 'definitions': definitions}


def _build_state_schema(definitions):
    return {'$ref': '#/definitions/State', 'definitions': definitions}
