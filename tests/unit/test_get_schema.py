from unittest import TestCase

from seizento.controllers.exceptions import Unauthorized, NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_get_property(self):
        self.test_client.set('/schema/test', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        response = self.test_client.get('/schema/test/a')

        self.assertEqual({'type': 'string'}, response)

    def test_get_nonexistent_property(self):
        self.test_client.set('/schema/test', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        with self.assertRaises(NotFound):
            self.test_client.get('/schema/test/b')

    def test_get_property_with_special_chars(self):
        self.test_client.set('/schema/test', {'type': 'object', 'properties': {'^&*(2 .$': {'type': 'string'}}})

        response = self.test_client.get('/schema/test/%5E%26%2A%282%20.%24')

        self.assertEqual({'type': 'string'}, response)

    def test_get_schema_after_setting_property_with_special_chars(self):
        self.test_client.set('/schema/test', {'type': 'object'})
        self.test_client.set('/schema/test/%5E%26%2A%282%20.%24', {'type': 'string'})

        response = self.test_client.get('/schema/test')

        self.assertEqual({'type': 'object', 'properties': {'^&*(2 .$': {'type': 'string'}}}, response)

    def test_empty(self):
        self.test_client.set('schema/test', {})

        response = self.test_client.get('schema/test')

        self.assertEqual({}, response)

    def test_no_additional_properties(self):
        self.test_client.set('schema/test', {'additionalProperties': False})

        response = self.test_client.get('schema/test')

        self.assertEqual({'additionalProperties': False}, response)

    def test_empty_property(self):
        self.test_client.set('schema/test', {'properties': {'a': {}}})

        response = self.test_client.get('schema/test')

        self.assertEqual({'properties': {'a': {}}}, response)

    def test_empty_items(self):
        self.test_client.set('schema/test', {'items': {}})

        response = self.test_client.get('schema/test/~items')

        self.assertEqual({}, response)

    def test_empty_additional_properties(self):
        self.test_client.set('schema/test', {'additionalProperties': {}})

        response = self.test_client.get('schema/test/~properties')

        self.assertEqual({}, response)

    def test_no_access(self):
        self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {
                    'read_access': ['schema/test/thing'],
                    'write_access': ['schema/test/thing']
                }
            }
        )
        self.test_client.set(
            '/schema/test',
            {
                'type': 'object',
                'properties': {
                    'thing': {'type': 'string'},
                    'other-thing': {'type': 'integer'}
                }
            }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'my-password'})

        with self.assertRaises(Unauthorized):
            self.test_client.get('schema/test/other-thing')
