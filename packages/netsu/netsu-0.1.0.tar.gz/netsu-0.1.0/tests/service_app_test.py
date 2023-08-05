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
import pytest

from flask import url_for

import netsu.core.errors
import netsu.service.app


@pytest.fixture
def MockedInterface(mocker):
    return mocker.patch('netsu.core.interface.Interface', autospec=True)


@pytest.fixture
def app(MockedInterface):
    return netsu.service.app.Application().app


class CoreTestError(netsu.core.errors.NetsuCoreError):
    """Foo Bar Baz"""
    CODE = 1


@pytest.mark.unit
@pytest.mark.usefixtures('client_class')
class TestApp(object):

    def _get(self, name):
        return self.client.get(url_for(name))

    def _put(self, name, data, parameters=None):
        request = {'data': data}
        if parameters:
            request['parameters'] = parameters
        return self.client.put(url_for(name), data=json.dumps(request),
                               content_type='application/json')

    def test_get_persistent_config(self, MockedInterface):
        DATA = {'foo': 'bar'}
        MockedInterface.return_value.get_persistent_config.return_value = DATA
        response = self._get('persistent_config')
        assert response.status_code == 200
        assert response.json['code'] == 0
        assert DATA == response.json['data']

    def test_put_persistent_config(self, MockedInterface):
        DATA = {'foo': 'bar'}
        response = self._put('persistent_config', DATA)
        assert response.status_code == 201
        MockedInterface.return_value.set_persistent_config.assert_called_with(
            DATA)

    def test_get_running_config(self, MockedInterface):
        DATA = {'foo': 'bar'}
        MockedInterface.return_value.get_running_config.return_value = DATA
        response = self._get('running_config')
        assert response.status_code == 200
        assert response.json['code'] == 0
        assert DATA == response.json['data']

    def test_set_running_config(self, MockedInterface, mocker):
        DATA = {'foo': 'bar'}
        PARAMETERS = {'Bar': 'baz'}
        response = self._put('running_config', DATA, PARAMETERS)
        assert response.status_code == 201
        call = MockedInterface.return_value.set_running_config.mock_calls[0][1]
        assert DATA == call[0]
        assert PARAMETERS == call[1]

    def test_set_running_config_setup_error(self, MockedInterface):
        MockedInterface.return_value.set_running_config.side_effect = \
            CoreTestError()
        response = self._put('running_config', data={}, parameters={})
        assert response.status_code == 520
        assert CoreTestError.__doc__ == response.json['message']

    def test_get_system_config(self, MockedInterface):
        DATA = {'foo': 'bar'}
        MockedInterface.return_value.get_system_config.return_value = DATA
        response = self._get('system_config')
        assert response.status_code == 200
        assert response.json['code'] == 0
        assert DATA == response.json['data']

    def test_get_system_config_error(self, MockedInterface):
        MockedInterface.return_value.get_system_config.side_effect = \
            CoreTestError()
        response = self._get('system_config')
        assert response.status_code == 520
        assert response.json['code'] == CoreTestError.CODE
        assert CoreTestError.__doc__ == response.json['message']

    def test_get_system_state(self, MockedInterface):
        DATA = {'foo': 'bar'}
        MockedInterface.return_value.get_system_state.return_value = DATA
        response = self._get('system_state')
        assert response.status_code == 200
        assert response.json['code'] == 0
        assert DATA == response.json['data']

    def test_get_system_state_error(self, MockedInterface):
        MockedInterface.return_value.get_system_state.side_effect = \
            CoreTestError()
        response = self._get('system_state')
        assert response.status_code == 520
        assert response.json['code'] == CoreTestError.CODE
        assert CoreTestError.__doc__ == response.json['message']
