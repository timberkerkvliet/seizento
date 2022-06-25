from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.test_interface.test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, 'a literal string')

    async def test_set_and_evaluate_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set('/expression/', 'a literal string')

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 9000)

    async def test_missing_value(self):
        await self.test_client.set('/schema/', {'type': 'string'})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation')
