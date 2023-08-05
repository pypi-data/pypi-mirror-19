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

from netsu.core import interface


pytestmark = pytest.mark.usefixtures('mocked_plugins')


@pytest.fixture
def mocked_plugins(mocker):
    mocker.patch.multiple(
        'netsu.core.plugins',
        get_definitions_updates=lambda: [],
        get_config_updates=lambda: [],
        get_state_updates=lambda: [],
        get_setup_steps=lambda: [],
        get_force_cleanup_steps=lambda: [])


@pytest.fixture
def MockedPersistentConfig(mocker):
    return mocker.patch.object(
        interface.data, 'PersistentConfig', autospec=True)


@pytest.fixture
def MockedRunningConfig(mocker):
    return mocker.patch.object(interface.data, 'RunningConfig', autospec=True)


@pytest.fixture
def MockedSystemConfig(mocker):
    return mocker.patch.object(interface.data, 'SystemConfig', autospec=True)


@pytest.fixture
def MockedSystemState(mocker):
    return mocker.patch.object(interface.data, 'SystemState', autospec=True)


@pytest.fixture
def MockedConfigurator(mocker):
    return mocker.patch.object(
        interface.configurator, 'Configurator', autospec=True)


@pytest.mark.unit
class TestInterfacePersistenConfig(object):

    def test_get_persistent_config(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        MockedPersistentConfig.return_value.get.return_value = {}
        iface = interface.Interface()
        persistent_config = iface.get_persistent_config()
        assert {} == persistent_config

    def test_set_persistent_config(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        iface = interface.Interface()
        iface.set_persistent_config({})
        MockedPersistentConfig.return_value.set.assert_called_with({})


@pytest.mark.unit
class TestInterfaceRunningConfig(object):

    REQUEST_CONFIG = {'a': 1}
    PARAMETERS = {'b': 2}

    @pytest.fixture(autouse=True)
    def mock_lock_file_path(self, mocker, tmpdir):
        mocker.patch.object(
            interface, 'SET_RUNNING_CONFIG_LOCK_PATH',
            str(tmpdir.join(
                os.path.basename(interface.SET_RUNNING_CONFIG_LOCK_PATH))))

    def test_get_running_config(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        MockedRunningConfig.return_value.get.return_value = {}
        iface = interface.Interface()
        running_config = iface.get_running_config()
        assert {} == running_config

    def test_set_running_config(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        iface = interface.Interface()
        iface.set_running_config(self.REQUEST_CONFIG, self.PARAMETERS)
        MockedConfigurator.return_value.run.assert_called_with(
            self.REQUEST_CONFIG, self.PARAMETERS)
        MockedRunningConfig.return_value.set.assert_called_with(
            self.REQUEST_CONFIG)

    def test_set_running_config_is_synchronous(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        SLEEP = 0.1
        MockedConfigurator.return_value.run.side_effect = \
            lambda *args, **kwargs: sleep(SLEEP)
        iface = interface.Interface()
        thread_a = Thread(target=iface.set_running_config, args=({}, {}))
        thread_b = Thread(target=iface.set_running_config, args=({}, {}))
        time_start = os.times()[4]
        thread_a.start()
        thread_b.start()
        thread_a.join()
        thread_b.join()
        time_stop = os.times()[4]
        assert time_stop - time_start > 1.9 * SLEEP


@pytest.mark.unit
class TestInterfaceSystemConfig(object):

    def test_get_system_config(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        MockedSystemConfig.return_value.get.return_value = {}
        iface = interface.Interface()
        system_config = iface.get_system_config()
        assert {} == system_config


@pytest.mark.unit
class TestInterfaceSystemState(object):

    def test_get_system_state(
            self, MockedPersistentConfig, MockedRunningConfig,
            MockedSystemConfig, MockedSystemState, MockedConfigurator):
        MockedSystemState.return_value.get.return_value = {}
        iface = interface.Interface()
        system_state = iface.get_system_state()
        assert {} == system_state
