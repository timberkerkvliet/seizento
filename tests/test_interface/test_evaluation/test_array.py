from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_interface.test_client import UnitTestClient


class TestArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, 2, 3, 4])
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 2, 3, 4])
