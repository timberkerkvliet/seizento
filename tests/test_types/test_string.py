from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_string(self):
        await self.test_client.set(
            '/schema/',
            {'name': 'STRING'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'name': 'STRING'})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'name': 'STRING'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'name': 'INTEGER'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'name': 'STRING'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'name': 'INTEGER'}
            )
