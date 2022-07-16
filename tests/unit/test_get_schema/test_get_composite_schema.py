from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetCompositeSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_struct_schema_is_persisted(self):
        self.test_client.set(
            'schema/test',
            {
                'type': ['array', 'object'],
                'properties': {'a': {'type': 'integer'}},
                'additionalProperties': {'type': 'string'},
                'items': {'type': 'boolean'}
            }
        )

        response = self.test_client.get('schema/test')

        self.assertEqual({'array', 'object'}, set(response['type']))
        self.assertEqual({'a': {'type': 'integer'}}, response['properties'])
        self.assertEqual({'type': 'string'}, response['additionalProperties'])
        self.assertEqual({'type': 'boolean'}, response['items'])


