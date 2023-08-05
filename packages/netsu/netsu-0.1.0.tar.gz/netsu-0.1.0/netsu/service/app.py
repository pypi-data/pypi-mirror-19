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

import flask

import netsu.core.errors
import netsu.core.interface


LOGGING_LEVEL_ENV_VARIABLE = 'NETSU_LOGGING_LEVEL'


class Application(object):

    def __init__(self):
        _initialize_logging()

        self.app = flask.Flask(__name__)
        self._core_interface = netsu.core.interface.Interface()

        self.app.add_url_rule(
            '/v1/persistent/config', self.persistent_config.__name__,
            self.persistent_config, methods=('GET', 'PUT'))
        self.app.add_url_rule(
            '/v1/running/config', self.running_config.__name__,
            self.running_config, methods=('GET', 'PUT'))
        self.app.add_url_rule(
            '/v1/system/config', self.system_config.__name__,
            self.system_config, methods=('GET',))
        self.app.add_url_rule(
            '/v1/system/state', self.system_state.__name__,
            self.system_state, methods=('GET',))

    def persistent_config(self):
        if flask.request.method == 'GET':
            return LoadedResponse(self._core_interface.get_persistent_config())
        elif flask.request.method == 'PUT':
            requested_config = flask.request.get_json()['data']
            try:
                self._core_interface.set_persistent_config(requested_config)
            except netsu.core.errors.NetsuCoreError as e:
                return CoreErrorResponse(e)
            else:
                return CreatedResponse()

    def running_config(self):
        if flask.request.method == 'GET':
            return LoadedResponse(self._core_interface.get_running_config())
        elif flask.request.method == 'PUT':
            request = flask.request.get_json()
            requested_config = request['data']
            request_parameters = request.get('parameters', {})
            try:
                self._core_interface.set_running_config(
                    requested_config, request_parameters)
            except netsu.core.errors.NetsuCoreError as e:
                return CoreErrorResponse(e)
            else:
                return CreatedResponse()

    def system_config(self):
        try:
            return LoadedResponse(self._core_interface.get_system_config())
        except netsu.core.errors.NetsuCoreError as e:
            return CoreErrorResponse(e)

    def system_state(self):
        try:
            return LoadedResponse(self._core_interface.get_system_state())
        except netsu.core.errors.NetsuCoreError as e:
            return CoreErrorResponse(e)


class JsonResponse(flask.Response):
    def __init__(self, data, status):
        super().__init__(json.dumps(data), status=status,
                         content_type='application/json')


class LoadedResponse(JsonResponse):
    STATUS = 200

    def __init__(self, data):
        super().__init__({'code': 0, 'message': 'Success', 'data': data},
                         LoadedResponse.STATUS)


class CreatedResponse(JsonResponse):
    STATUS = 201

    def __init__(self):
        super().__init__({'code': 0, 'message': 'Success'},
                         CreatedResponse.STATUS)


class CoreErrorResponse(JsonResponse):
    STATUS = 520

    def __init__(self, core_error_instance):
        super().__init__({'code': core_error_instance.CODE,
                          'message': core_error_instance.__doc__},
                         CoreErrorResponse.STATUS)


def _initialize_logging():
    logging_level = os.environ.get(LOGGING_LEVEL_ENV_VARIABLE, 'INFO')
    logging.basicConfig(level=logging_level)
