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

from pprint import pprint
import argparse
import json
import sys

import requests


DEFAULT_SERVICE_ADDRESS = 'http://127.0.0.1:59872'

WRITABLE_CONFIG_TABLES = {'persistent-config', 'running-config'}
READABLE_CONFIG_TABLES = WRITABLE_CONFIG_TABLES | {'system-config'}
READABLE_TABLES = READABLE_CONFIG_TABLES | {'system-state'}


def request_get(service, source_name):
    url = '{}/v1/{}'.format(service, _name_to_url(source_name))
    return requests.get(url, headers={'content-type': 'application/json'})


def request_put(service, source_name, data, parameters):
    url = '{}/v1/{}'.format(service, _name_to_url(source_name))
    return requests.put(url, json={'data': data, 'parameters': parameters})


def _name_to_url(name):
    return name.replace('-', '/')


def _format_invalid_choice_error(choice, choices):
    return "argument DATA: invalid choice: '{}' (choose from {})".format(
        choice, _quotes_and_commas(choices))


def _quotes_and_commas(items):
    return ', '.join(["'{}'".format(item) for item in items])


def _print_and_exit(response, pretty):
    if pretty:
        pprint(response)
    else:
        print(json.dumps(response))
    if response['code'] == 0:
        sys.exit(0)
    else:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog='netsu-ctl')

    parser.add_argument('--service-address', default=DEFAULT_SERVICE_ADDRESS)
    parser.add_argument('--pretty', action='store_true')

    subparsers = parser.add_subparsers(dest='COMMAND')

    parser_get = subparsers.add_parser('get')
    parser_get.add_argument('TABLE', choices=READABLE_TABLES)

    parser_set = subparsers.add_parser('set')
    parser_set.add_argument('--copy-from-table', action='store_true')
    parser_set.add_argument('TABLE', choices=WRITABLE_CONFIG_TABLES)
    parser_set.add_argument(
        'DATA', type=str,
        help='data in JSON format or name of source table if '
             '--copy-from-table is set.')
    parser_set.add_argument('PARAMETERS', type=str, nargs='?', default='{}')

    args = parser.parse_args()
    if args.COMMAND == 'get':
        response = request_get(args.service_address, args.TABLE).json()
        _print_and_exit(response, args.pretty)
    elif args.COMMAND == 'set':
        if args.copy_from_table:
            if args.DATA not in READABLE_CONFIG_TABLES:
                parser.error(_format_invalid_choice_error(
                    args.DATA, READABLE_CONFIG_TABLES))
            response = request_get(args.service_address, args.DATA)
            response.raise_for_status()
            data = response.json()['data']
        else:
            data = json.loads(args.DATA)
        parameters = json.loads(args.PARAMETERS)
        response = request_put(
            args.service_address, args.TABLE, data, parameters).json()
        _print_and_exit(response, args.pretty)
    else:
        parser.error('COMMAND is required.')
