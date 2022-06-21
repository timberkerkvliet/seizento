from unittest import IsolatedAsyncioTestCase, skip

from tests.test_client import UnitTestClient


class TestArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/type/', {'name': 'ARRAY', 'value_type': {'name': 'INTEGER'}})
        await self.test_client.set(
            '/expression/',
            [1, 2, 3, 4]
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])

    async def test_set_and_empty_literal(self):
        await self.test_client.set('/type/', {'name': 'ARRAY', 'value_type': {'name': 'INTEGER'}})
        await self.test_client.set('/expression/', [])

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [])

    @skip
    async def test_set_per_index(self):
        await self.test_client.set('/type/', {'name': 'ARRAY', 'value_type': {'name': 'INTEGER'}})
        await self.test_client.set('/expression/0', 1)
        await self.test_client.set('/expression/1', 2)
        await self.test_client.set('/expression/2', 3)
        await self.test_client.set('/expression/3', 4)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])
