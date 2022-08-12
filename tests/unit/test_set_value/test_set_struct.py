from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestStruct(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set(
            '/value/test/',
            {'a': 1001, 'b': 'nachten'}
        )
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'a': 1001, 'b': 'nachten'})

    def test_set_partially(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set(
            '/value/test/',
            {'a': 1001}
        )
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'a': 1001})

    def test_empty(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set('/value/test/', {})
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {})

    def test_get_field_value(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'}
                }
            }
        )
        self.test_client.set('/value/test/', {'a': 9})

        response = self.test_client.get('value/test/a')

        self.assertEqual(response, 9)

    def test_nested_struct(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'object',
                        'properties': {
                            'b': {'type': 'integer'}
                        }
                    }
                }
            }
        )
        self.test_client.set('/value/test', {'a': {'b': 99}})

        response = self.test_client.get('/value/test/a/b')

        self.assertEqual(response, 99)

    def test_given_a_non_literal_parent_value_when_setting_value_then_raise_forbidden(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'array', 'items': {'type': 'integer'}},
                    'b': {'type': 'array', 'items': {'type': 'integer'}}
                }
            }
        )
        self.test_client.set(
            '/value/test',
            {
                'a': [1, 2, 3, 4],
                'b': '{/test/a}'
            }
        )

        with self.assertRaises(Forbidden):
            self.test_client.set('/value/test/b/0', 5)

    def test_when_setting_value_with_no_paren_then_raise_not_found(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        with self.assertRaises(NotFound):
            self.test_client.set('/value/test/a', 99)

    def test_add_field_after_value_has_been_set(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        self.test_client.set('/value/test', {'a': 19})
        self.test_client.set('/schema/test/b', {'type': 'string'})
        self.test_client.set('/value/test/b', 'hallo')

        response = self.test_client.get('value/test')

        self.assertDictEqual({'a': 19, 'b': 'hallo'}, response)

    def test_adding_field_to_root_value(self):
        with self.assertRaises(Forbidden):
            self.test_client.set('/value/some-thing', 9)

    def test_setting_value(self):
        with self.assertRaises(Forbidden):
            self.test_client.set('/value', {})
