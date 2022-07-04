from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.test_client import UnitTestClient


class TestInteger(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'integer'})
        await self.test_client.set(
            '/expression/',
            -7
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, -7)

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 8.77)
