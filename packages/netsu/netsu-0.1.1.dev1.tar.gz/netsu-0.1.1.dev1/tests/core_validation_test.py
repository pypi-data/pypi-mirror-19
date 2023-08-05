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

import copy
import pytest

from netsu.core import validation


@pytest.mark.unit
class TestValidateData(object):

    SCHEMA = {
        'type': 'object',
        'properties': {
            'foo': {
                'type': 'string'
            }
        }
    }

    def test_valid_data(self):
        DATA = {'foo': 'bar'}
        validation.Validator(self.SCHEMA).validate(DATA)

    def test_invalid_data(self):
        DATA = {'foo': 123}
        with pytest.raises(validation.ValidationError):
            validation.Validator(self.SCHEMA).validate(DATA)


@pytest.mark.unit
class TestFillInDefaults(object):

    SCHEMA = {
        'type': 'object',
        'properties': {
            'outer-object': {
                'type': 'object',
                'default': {},
                'properties': {
                    'inner-object': {
                        'type': 'string',
                        'default': 'DEFAULTS'
                    }
                }
            }
        }
    }
    DEFAULTS = {'outer-object': {'inner-object': 'DEFAULTS'}}

    def test_fill_in_defaults(self):
        data = {}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.DEFAULTS == data

    def test_keep_given_data(self):
        DATA = {'outer-object': {'inner-object': 'shruberry'}}
        data = copy.deepcopy(DATA)
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert DATA == data


@pytest.mark.unit
class TestFillInDefaultsFromBuiltSchema(object):

    SCHEMA = {
        '$ref': '#/definitions/Data',
        'definitions': {
            'Data': {
                'type': 'object',
                'default': {},
                'properties': {
                    'outer-object': {
                        '$ref': '#/definitions/OuterObject'
                    }
                }
            },
            'OuterObject': {
                'type': 'object',
                'default': {},
                'properties': {
                    'inner-object': {
                        '$ref': '#/definitions/InnerObject'
                    }
                }
            },
            'InnerObject': {
                'type': 'string',
                'default': 'DEFAULTS'
            }
        }
    }
    DEFAULTS = {'outer-object': {'inner-object': 'DEFAULTS'}}

    def test_fill_in_defaults(self):
        data = {}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.DEFAULTS == data

    def test_keep_given_data(self):
        DATA = {'outer-object': {'inner-object': 'shruberry'}}
        data = copy.deepcopy(DATA)
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert DATA == data


@pytest.mark.unit
class TestFillInDefaultsToList(object):

    SCHEMA = {
        'type': 'object',
        'properties': {
            'outer-object': {
                'type': 'object',
                'default': {},
                'properties': {
                    'inner-object': {
                        'type': 'array',
                        'default': [],
                        'items': {
                            'type': 'object',
                            'properties': {
                                'list-object': {
                                    'default': 'DEFAULTS',
                                    'type': 'string'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    DEFAULTS = {'outer-object': {'inner-object': []}}
    OBJECT_IN_LIST_DEFAULTS = {
        'outer-object': {'inner-object': [{'list-object': 'DEFAULTS'}]}}

    def test_fill_in_defaults(self):
        data = {}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.DEFAULTS == data

    def test_fill_in_object_in_list_defaults(self):
        data = {'outer-object': {'inner-object': [{}]}}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.OBJECT_IN_LIST_DEFAULTS == data

    def test_keep_given_data(self):
        DATA = {'outer-object': {'inner-object': [{'list-object': 'foo'}]}}
        data = copy.deepcopy(DATA)
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert DATA == data


@pytest.mark.unit
class TestFillInDefaultsToPatternProperties(object):

    SCHEMA = {
        'type': 'object',
        'properties': {
            'outer-object': {
                'type': 'object',
                'default': {},
                'patternProperties': {
                    '^[a-z-]{1,16}$': {
                        'type': 'object',
                        'properties': {
                            'list-object': {
                                'default': 'DEFAULTS',
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        }
    }
    DEFAULTS = {'outer-object': {}}
    PROPERTY_IN_OBJECT_DEFAULTS = {
        'outer-object': {'inner-object': {'list-object': 'DEFAULTS'}}}

    def test_fill_in_defaults(self):
        data = {}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.DEFAULTS == data

    def test_fill_in_property_in_object_defaults(self):
        data = {'outer-object': {'inner-object': {}}}
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert self.PROPERTY_IN_OBJECT_DEFAULTS == data

    def test_keep_given_data(self):
        DATA = {'outer-object': {'inner-object': {'list-object': 'foo'}}}
        data = copy.deepcopy(DATA)
        validation.Validator(self.SCHEMA).validate_and_set_defaults(data)
        assert DATA == data
