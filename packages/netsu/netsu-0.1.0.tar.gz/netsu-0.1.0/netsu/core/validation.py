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

import jsonschema


class ValidationError(jsonschema.ValidationError):
    """Data validation failed"""
    CODE = 41


class Validator(object):

    def __init__(self, schema):
        logging.info('Initializing Validator with {}'.format(schema))
        self._validator = jsonschema.Draft4Validator(schema)
        self._validator_with_defaults = \
            _extend_with_set_defaults(jsonschema.Draft4Validator)(schema)

    def validate(self, data):
        _validate(self._validator, data)

    def validate_and_set_defaults(self, data):
        _validate(self._validator_with_defaults, data)


def _validate(validator, data):
    try:
        validator.validate(data)
    except jsonschema.ValidationError as e:
        raise ValidationError('Invalid data: {}'.format(data)) from e


def _extend_with_set_defaults(validator_class):
    validate_properties = validator_class.VALIDATORS['properties']

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():

            if '$ref' in subschema:
                definition = validator.resolver.resolve(subschema['$ref'])[1]
            else:
                definition = subschema

            if 'default' in definition:
                instance.setdefault(property, definition['default'])

        for error in validate_properties(
                validator, properties, instance, schema):
            yield error

    return jsonschema.validators.extend(
        validator_class, {'properties': set_defaults})
