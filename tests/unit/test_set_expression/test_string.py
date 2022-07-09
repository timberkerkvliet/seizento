from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, 'a literal string')

    async def test_set_null(self):
        await self.test_client.set('/schema/', {'type': ['string', 'null']})
        await self.test_client.set('/expression/', None)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, None)

    async def test_set_wrong_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 9000)
