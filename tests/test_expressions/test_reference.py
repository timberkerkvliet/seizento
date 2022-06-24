from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestReference(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1])

        await self.test_client.set('/expression/1', '{/0}')

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1])
