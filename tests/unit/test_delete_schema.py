from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestDeleteSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_delete_property(self):
        self.test_client.set('schema/test', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        self.test_client.delete('/schema/test/a')

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(
            response,
            {'type': 'object', 'properties': {}}
        )

    def test_delete_invalidating_value(self):
        self.test_client.set(
            'schema/test',
            {'type': 'object', 'properties': {'a': {'type': 'string'}}, 'additionalProperties': False})

        self.test_client.set('value/test', {'a': 'a'})

        with self.assertRaises(Forbidden):
            self.test_client.delete('/schema/test/a')

    def test_delete_nonexisting_property(self):
        self.test_client.set('/schema/test', {'type': 'object'})
        self.test_client.delete('/schema/test/a')

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )
