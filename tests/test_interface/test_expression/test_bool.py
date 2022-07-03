from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.test_interface.test_client import UnitTestClient


class TestBool(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})
        await self.test_client.set(
            '/expression/',
            True
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, True)

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 9000)
