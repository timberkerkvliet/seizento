from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, BadRequest
from tests.test_client import UnitTestClient


class TestStringTypeContext(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()
        await self.test_client.set(
            '/type/',
            {'name': 'STRING'}
        )

    async def test_set_and_get_literal(self):
        await self.test_client.set(
            '/expression/',
            {'literal': 'a literal string'}
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, {'literal': 'a literal string'})

    async def test_set_and_evaluate_literal(self):
        await self.test_client.set(
            '/expression/',
            {'literal': 'a literal string'}
        )
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    async def test_set_wrong_literal(self):
        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/expression/',
                {'literal': 9000}
            )

    async def test_cannot_set_child(self):
        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/type/a',
                {'name': 'INTEGER'}
            )

    async def test_cannot_set_placeholder_child(self):
        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/type/~',
                {'name': 'INTEGER'}
            )
