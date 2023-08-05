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

import inspect
import logging

from . import errors


class SetupError(errors.NetsuCoreError):
    """Setup failed, but we were able to rollback to initial state"""
    CODE = 31


class CriticalSetupError(errors.NetsuCoreError):
    """Setup failed, we were able to cleanup all configuration"""
    CODE = 32


class FatalSetupError(errors.NetsuCoreError):
    """Setup failed, configuration was left in inconsistent state"""
    CODE = 33


class Configurator(object):
    def __init__(self, setup_steps, force_cleanup_steps, running_config,
                 system_config):
        logging.info(
            'Initializing Configurator with setup steps {} and force '
            'cleanup steps {}'.format(
                ['{}:{}'.format(step.__module__, step.__name__)
                 for step in setup_steps],
                ['{}:{}'.format(step.__module__, step.__name__)
                 for step in force_cleanup_steps]))
        self._setup_steps = setup_steps
        self._force_cleanup_steps = force_cleanup_steps
        self._running_config = running_config
        self._system_config = system_config

    def run(self, requested_config, parameters):
        logging.debug('Setting up config {} with parameters {}'.format(
            requested_config, parameters))
        try:
            self._run(requested_config, parameters)
        except:
            logging.exception('Setup failed with:')
            raise

    def _run(self, requested_config, parameters):
        try:
            self._setup(requested_config, parameters)
        except Exception as setup_e:
            logging.error('Setup attempt failed, running soft rollback')
            try:
                self._soft_rollback()
            except Exception as soft_rollback_e:
                logging.error('Soft rollback failed, trying harder')
                try:
                    self._hard_rollback()
                except Exception as hard_rollback_e:
                    logging.error('All rollback attempts failed, trying to '
                                  'clean up all configuration')
                    try:
                        self._cleanup()
                    except Exception as cleanup_e:
                        logging.error('Configuration cleanup failed')
                        raise FatalSetupError() from cleanup_e
                    raise CriticalSetupError() from hard_rollback_e
                raise SetupError() from soft_rollback_e
            raise SetupError() from setup_e

    def _setup(self, requested_config, parameters):
        self._run_setup(requested_config, parameters)
        self._check_expected_config(requested_config)

    def _soft_rollback(self):
        self._run_setup(self._running_config.get())
        self._check_expected_config(self._running_config.get())

    def _hard_rollback(self):
        self._run_force_cleanup()
        self._run_setup(self._running_config.get())
        self._check_expected_config(self._running_config.get())

    def _cleanup(self):
        self._run_force_cleanup()
        self._check_expected_config({})

    def _run_setup(self, requested_config, parameters=None):
        for setup_step in self._setup_steps:
            _run_function_with_demanded_arguments(
                setup_step,
                available_arguments={
                    'requested_config': requested_config,
                    'parameters': parameters or {}
                },
                available_callable_arguments={
                    'system_config': self._system_config.get
                })

    def _run_force_cleanup(self):
        for force_cleanup_step in self._force_cleanup_steps:
            force_cleanup_step()

    def _check_expected_config(self, expected_config):
        system_config = self._system_config.get()
        if system_config != expected_config:
            raise AssertionError(
                'Current system config does not match expected config:\n'
                'system config:\n{}\n'
                'expected config:\n{}'.format(system_config, expected_config))


def _run_function_with_demanded_arguments(
        function, available_arguments, available_callable_arguments):
    demanded_parameters = inspect.signature(function).parameters.keys()
    kwargs = {
        demanded_parameter: (
            available_callable_arguments[demanded_parameter]()
            if demanded_parameter in available_callable_arguments
            else available_arguments[demanded_parameter])
        for demanded_parameter in demanded_parameters}
    logging.debug('Executing {}:{} with {}'.format(
        function.__module__, function.__name__, kwargs))
    function(**kwargs)
