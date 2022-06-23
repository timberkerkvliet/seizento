from unittest import IsolatedAsyncioTestCase, skip

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        await self.test_client.set(
            '/expression/',
            {'a': 1001, 'b': 'nachten'}
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, {'a': 1001, 'b': 'nachten'})
