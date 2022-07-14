from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestStruct(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_struct_schema_is_persisted(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'integer'}
            },
            'additionalProperties': False
        }
        self.test_client.set('/schema/', schema)

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response, schema)

    def test_reset_struct_schema_is_persisted(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}},
                'additionalProperties': False
            }
        )

        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'b': {'type': 'integer'}},
                'additionalProperties': False
            }
        )

        response = self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'b': {'type': 'integer'}
                },
                'additionalProperties': False
            }
        )

    def test_adding_fields(self):
        self.test_client.set('schema/', {'type': 'object', 'additionalProperties': False})

        self.test_client.set(
            '/schema/c',
            {'type': 'integer'}
        )
        self.test_client.set(
            '/schema/d',
            {'type': 'string'}
        )

        response = self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'c': {'type': 'integer'},
                    'd': {'type': 'string'}
                },
                'additionalProperties': False
            }
        )

    def test_extending_fields(self):
        self.test_client.set(
            '/schema/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}, 'additionalProperties': False}
        )
        self.test_client.set('/expression/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            },
            'additionalProperties': False
        }

        self.test_client.set('/schema/', new_schema)

        response = self.test_client.get('/schema')

        self.assertDictEqual(response, new_schema)

    def test_set_field_name_with_special_chars(self):
        try:
            self.test_client.set(
                '/schema',
                {'type': 'object', 'properties': {'^ (&@a9.?$#/{é': {'type': 'string'}}, 'additionalProperties': False}
            )
        except BadRequest:
            self.fail()

    def test_set_struct_from_dict(self):
        self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        self.test_client.set('/expression', {'a': 'a'})

        try:
            self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'properties': {'a': {'type': 'string'}},
                    'additionalProperties': False
                }
            )
        except Forbidden:
            self.fail()

    def test_set_struct_from_dict_with_nested(self):
        self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'string'},
                        'b': {'type': 'integer'}
                    },
                    'additionalProperties': False
                }
            }
        )
        self.test_client.set('/expression', {'Ti': {'a': 'string'}})

        try:
            self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'string'},
                            'c': {'type': 'integer'}
                        },
                        'additionalProperties': False
                    }
                }
            )
        except Forbidden:
            self.fail()

    def test_cannot_set_struct_from_dict_with_nested(self):
        self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'string'},
                        'b': {'type': 'integer'}
                    },
                    'additionalProperties': False
                }
            }
        )
        self.test_client.set('/expression', {'Ti': {'a': 'string'}})

        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'integer'},
                            'c': {'type': 'integer'}
                        },
                        'additionalProperties': False
                    }
                }
            )

    def test_set_struct_from_dict_if_empty_is_set(self):
        self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        self.test_client.set('/expression', {})

        try:
            self.test_client.set(
                '/schema',
                {'type': 'object', 'properties': {'a': {'type': 'string'}}, 'additionalProperties': False}
            )
        except Forbidden:
            self.fail()

    def test_set_struct_from_non_matching_dict(self):
        self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        self.test_client.set('/expression', {'b': 'b'})

        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'properties': {'a': {'type': 'string'}},
                    'additionalProperties': False
                }
            )
