from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import BadRequest
from tests.test_client import UnitTestClient


class TestFunction(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_function(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'children': {'~': {'name': 'INTEGER'}}}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'children': {
                    '~': {'name': 'INTEGER'}
                }
            }
        )

    async def test_set_value_type(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'children': {'~': {'name': 'INTEGER'}}}
        )
        await self.test_client.set('/type/~/', {'name': 'FLOAT'})

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'children': {'~': {'name': 'FLOAT'}}
            }
        )

    async def test_set_function_without_children(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                '/type/',
                {'name': 'FUNCTION'}
            )

    async def test_set_function_without_placeholder(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                '/type/',
                {'name': 'FUNCTION', 'children': {'a': {'name': 'INTEGER'}}}
            )
