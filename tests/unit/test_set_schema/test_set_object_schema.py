from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetObject(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

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
