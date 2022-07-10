import math
from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetFloatEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set(self):
        await self.test_client.set('/schema/', {'type': 'number'})
        await self.test_client.set('/expression/', -4.56)

        response = await self.test_client.get('/evaluation/')
        self.assertTrue(math.isclose(response, -4.56))

    async def test_not_set(self):
        await self.test_client.set('/schema/', {'type': 'number'})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation')
