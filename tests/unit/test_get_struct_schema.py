from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetStructSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_get_field_schema(self):
        self.test_client.set('/schema', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        response = self.test_client.get('/schema/a')

        self.assertEqual({'type': 'string'}, response)

    def test_get_field_schema_with_special_chars(self):
        self.test_client.set('/schema', {'type': 'object', 'properties': {'^&*(2 .$': {'type': 'string'}}})

        response = self.test_client.get('/schema/%5E%26%2A%282%20.%24')

        self.assertEqual({'type': 'string'}, response)

    def test_get_schema_after_setting_field_with_special_chars(self):
        self.test_client.set('/schema', {'type': 'object'})
        self.test_client.set('/schema/%5E%26%2A%282%20.%24', {'type': 'string'})

        response = self.test_client.get('/schema')

        self.assertEqual({'type': 'object', 'properties': {'^&*(2 .$': {'type': 'string'}}}, response)
