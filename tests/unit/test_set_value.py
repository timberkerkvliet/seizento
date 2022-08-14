from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetValue(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_basic_set(self):
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
            {'a': 1001, 'b': 'nachten', 'c': 'extra'}
        )
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'a': 1001, 'b': 'nachten', 'c': 'extra'})

    def test_set_array(self):
        self.test_client.set(
            'schema/test',
            {'type': 'array'}
        )
        self.test_client.set('value/test', [1, 'a', {'y': {'a': 'a'}}])

        response = self.test_client.get('value/test')

        self.assertEqual([1, 'a', {'y': {'a': 'a'}}], response)

    def test_set_invalid_array(self):
        self.test_client.set(
            'schema/test',
            {'type': 'array', 'items': {'enum': [1, 'a']}}
        )

        with self.assertRaises(Forbidden):
            self.test_client.set('value/test', [1, 'a', {'y': {'a': 'a'}}])

    def test_set_invalid_value(self):
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
        with self.assertRaises(Forbidden):
            self.test_client.set('value/test', {'a': 19, 'b': 20})

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

    def test_set_empty(self):
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

    def test_nested_object(self):
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

    def test_setting_property_with_parent_not_set(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        with self.assertRaises(NotFound):
            self.test_client.set('/value/test/a', 99)

    def test_set_property_type_after_value_has_been_set(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        self.test_client.set('/value/test', {'a': 19})
        self.test_client.set('/schema/test/b', {'type': 'string'})
        self.test_client.set('/value/test/b', 'hallo')

        response = self.test_client.get('value/test')

        self.assertDictEqual({'a': 19, 'b': 'hallo'}, response)

    def test_setting_root_value(self):
        with self.assertRaises(Forbidden):
            self.test_client.set('/value', {})
