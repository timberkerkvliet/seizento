from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetObject(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_add_additional_field(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'integer'}
            }
        }
        self.test_client.set('schema', schema)
        self.test_client.set('/schema/new-one', {'type': 'string'})

        response = self.test_client.get('/schema/')
        self.assertEqual(set(response['properties']), {'a', 'b', 'new-one'})
