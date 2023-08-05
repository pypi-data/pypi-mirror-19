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

from netsu.core import configurator
from netsu.core import data


@pytest.mark.unit
class TestConfigurator(object):

    def test_successful_setup(self, mocker):
        REQUEST_CONFIG = {'a': 1}
        PARAMETERS = {'b': 2}

        MockedRunningConfig = mocker.patch.object(data, 'RunningConfig')
        MockedRunningConfig.return_value.get.return_value = {}
        MockedSystemConfig = mocker.patch.object(data, 'SystemConfig')
        MockedSystemConfig.return_value.get.return_value = REQUEST_CONFIG

        # mock cannot be used with introspection
        setup_step_called_with = {}

        def setup_step(requested_config, system_config, parameters):
            setup_step_called_with['requested_config'] = requested_config
            setup_step_called_with['system_config'] = system_config

        _configurator = configurator.Configurator(
            [setup_step], [], MockedRunningConfig(), MockedSystemConfig())
        _configurator.run(REQUEST_CONFIG, PARAMETERS)

        assert ({'requested_config': REQUEST_CONFIG,
                 'system_config': REQUEST_CONFIG} ==
                setup_step_called_with)

    def test_failed_setup_with_cleanup(self, mocker):
        REQUEST_CONFIG = {'a': 1}
        PARAMETERS = {'b': 2}

        MockedRunningConfig = mocker.patch.object(data, 'RunningConfig')
        MockedRunningConfig.return_value.get.return_value = {}
        MockedSystemConfig = mocker.patch.object(data, 'SystemConfig')
        MockedSystemConfig.return_value.get.return_value = {}

        mocked_force_cleanup_step = mocker.Mock(lambda: None)

        _configurator = configurator.Configurator(
            [], [mocked_force_cleanup_step], MockedRunningConfig(),
            MockedSystemConfig())
        # we should not mock methods of tested instance, but in this case it is
        # not that bad as we are testing upper layers of the class
        _configurator._setup = mocker.Mock(side_effect=Exception())
        _configurator._soft_rollback = mocker.Mock(side_effect=Exception())
        _configurator._hard_rollback = mocker.Mock(side_effect=Exception())

        with pytest.raises(configurator.CriticalSetupError):
            _configurator.run(REQUEST_CONFIG, PARAMETERS)

        assert mocked_force_cleanup_step.called
