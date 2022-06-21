from unittest import IsolatedAsyncioTestCase, skip

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/type/', {'name': 'ARRAY', 'children': {'~': {'name': 'INTEGER'}}})
        await self.test_client.set(
            '/expression/',
            [1, 2, 3, 4]
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])
