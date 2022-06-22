from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import BadRequest
from tests.test_client import UnitTestClient


class TestFunction(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_function(self):
        await self.test_client.set(
            '/schema/',
            {'name': 'FUNCTION', 'value_type': {'name': 'INTEGER'}}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'value_type': {'name': 'INTEGER'}
            }
        )

    async def test_set_value_type(self):
        await self.test_client.set(
            '/schema/',
            {'name': 'FUNCTION', 'value_type': {'name': 'INTEGER'}}
        )
        await self.test_client.set('/schema/~/', {'name': 'FLOAT'})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'value_type': {'name': 'FLOAT'}
            }
        )

    async def test_set_function_without_value_type(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                '/schema/',
                {'name': 'FUNCTION'}
            )
