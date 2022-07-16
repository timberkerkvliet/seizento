from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetCompositeSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_multiple_types(self):
        self.test_client.set(
            'schema/test',
            {
                'type': ['array', 'object', 'string']
            }
        )

        response = self.test_client.get('schema/test')

        self.assertEqual({'array', 'object', 'string'}, set(response['type']))

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

        self.assertEqual({}, response)
