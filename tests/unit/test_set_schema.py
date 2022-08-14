from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden, Unauthorized
from tests.unit.unit_test_client import UnitTestClient


class TestSetSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_invalid_schema(self):
        with self.assertRaises(BadRequest):
            self.test_client.set('/schema/test', 'bloourh')

    def test_set(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'integer'}
            },
            'additionalProperties': False
        }
        self.test_client.set('/schema/test/', schema)

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, schema)

    def test_reset(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}},
                'additionalProperties': False
            }
        )

        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {'b': {'type': 'integer'}},
                'additionalProperties': True
            }
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'b': {'type': 'integer'}
                },
                'additionalProperties': True
            }
        )

    def test_add_fields(self):
        self.test_client.set('schema/test', {'type': 'object', 'additionalProperties': False})

        self.test_client.set(
            '/schema/test/c',
            {'type': 'integer'}
        )
        self.test_client.set(
            '/schema/test/d',
            {'type': 'string'}
        )

        response = self.test_client.get('/schema/test/')
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
            '/schema/test/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}, 'additionalProperties': False}
        )
        self.test_client.set('/value/test/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            },
            'additionalProperties': False
        }

        self.test_client.set('/schema/test/', new_schema)

        response = self.test_client.get('/schema/test')

        self.assertDictEqual(response, new_schema)

    def test_set_field_name_with_special_chars(self):
        try:
            self.test_client.set(
                '/schema/test',
                {'type': 'object', 'properties': {'^ (&@a9.?$#/{é': {'type': 'string'}}, 'additionalProperties': False}
            )
        except BadRequest:
            self.fail()

    def test_set_struct_from_dict(self):
        self.test_client.set('/schema/test', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        self.test_client.set('/value/test', {'a': 'a'})

        try:
            self.test_client.set(
                '/schema/test',
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
            '/schema/test',
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
        self.test_client.set('/value/test', {'Ti': {'a': 'string'}})

        try:
            self.test_client.set(
                '/schema/test',
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
            '/schema/test',
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
        self.test_client.set('/value/test', {'Ti': {'b': 15}})

        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/schema/test',
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

    def test_add_additional_field(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'integer'}
            }
        }
        self.test_client.set('schema/test', schema)
        self.test_client.set('/schema/test/new-one', {'type': 'string'})

        response = self.test_client.get('/schema/test/')
        self.assertEqual(set(response['properties']), {'a', 'b', 'new-one'})

    def test_set_dict(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'object', 'additionalProperties': {'type': 'string'}})

    def test_reset_value_type(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )
        self.test_client.set(
            '/schema/test/~properties',
            {'type': 'integer'}
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response,  {'type': 'object', 'additionalProperties': {'type': 'integer'}})

    def test_set_dict_from_struct(self):
        self.test_client.set(
            '/schema/test',
            {
                'type': 'object',
                'properties': {'a': {'type': 'string'}},
                'additionalProperties': False
            }
        )
        self.test_client.set('/value/test', {'a': 'a'})

        try:
            self.test_client.set('/schema/test', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        except Forbidden:
            self.fail()

    def test_can_set_authorized_schema(self):
        self.test_client.set(
            '/user/timber',
            {
                'access_rights': {
                    'read_access': [],
                    'write_access': ['schema/my-thing']
                },
                'password': 'a'
             }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'a'})

        try:
            self.test_client.set('schema/my-thing', {'type': 'string'})
        except Unauthorized:
            self.fail()

    def test_can_set_from_two_authorized_schemas(self):
        self.test_client.set(
            '/user/timber',
            {
                'access_rights': {
                    'read_access': [],
                    'write_access': ['schema/generic', 'schema/my-thing']
                },
                'password': 'a'
             }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'a'})

        try:
            self.test_client.set('schema/my-thing', {'type': 'string'})
        except Unauthorized:
            self.fail()
