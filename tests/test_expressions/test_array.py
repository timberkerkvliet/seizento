from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})
        await self.test_client.set(
            '/expression/',
            [1, 2, 3, 4]
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])

    async def test_set_and_empty_literal(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})
        await self.test_client.set('/expression/', [])

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [])

    async def test_reset_index(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})
        await self.test_client.set('/expression/', [1])
        await self.test_client.set('/expression/0', 2)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [2])

    async def test_add_index(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})
        await self.test_client.set('/expression/', [1])
        await self.test_client.set('/expression/1', 2)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2])

    async def test_set_wrong_type(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 1)

    async def test_set_wrong_value_type(self):
        await self.test_client.set('/schema/', {'type': 'ARRAY', 'value_type': {'type': 'INTEGER'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', ['a', 'b'])
