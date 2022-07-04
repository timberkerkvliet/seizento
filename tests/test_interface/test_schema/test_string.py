from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_interface.test_client import get_test_client


class TestString(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = get_test_client()

    async def test_set_string(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'string'})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )
