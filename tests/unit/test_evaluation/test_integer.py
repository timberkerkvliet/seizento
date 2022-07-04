from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.test_client import UnitTestClient


class TestInteger(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_positive(self):
        await self.test_client.set('/schema/', {'type': 'integer'})
        await self.test_client.set('/expression/', 10)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 10)

    async def test_set_zero(self):
        await self.test_client.set('/schema/', {'type': 'integer'})
        await self.test_client.set('/expression/', 0)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 0)

    async def test_set_negative(self):
        await self.test_client.set('/schema/', {'type': 'integer'})
        await self.test_client.set('/expression/', -100)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, -100)

    async def test_not_set(self):
        await self.test_client.set('/schema/', {'type': 'integer'})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation')
