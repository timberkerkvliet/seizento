from unittest import IsolatedAsyncioTestCase, skip

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'STRING'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, 'a literal string')

    async def test_set_and_evaluate_literal(self):
        await self.test_client.set('/schema/', {'type': 'STRING'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'STRING'})
        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/expression/',
                9000
            )

    async def test_get_null_as_default(self):
        await self.test_client.set('/schema/', {'type': 'STRING'})

        response = await self.test_client.get('/evaluation')

        self.assertIsNone(response)
