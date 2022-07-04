import math
from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.test_client import UnitTestClient


class TestFloat(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'number'})
        await self.test_client.set(
            '/expression/',
            9.998
        )
        response = await self.test_client.get('/expression/')
        self.assertTrue(math.isclose(response, 9.998))

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'number'})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 'hey')
