from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_interface.test_client import UnitTestClient


class TestSchemaChange(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_evaluation_after_change(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}}
        )
        await self.test_client.set('/expression/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            }
        }

        await self.test_client.set('/schema/', new_schema)

        response = await self.test_client.get('/evaluation')

        self.assertDictEqual(response, {'a': 900})
