from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestSetFunctionSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_function(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'subtypes': {'~': {'name': 'INTEGER'}}}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'subtypes': {
                    '~': {'name': 'INTEGER'}
                }
            }
        )

    async def test_set_value_type(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'subtypes': {'~': {'name': 'INTEGER'}}}
        )
        await self.test_client.set('/type/~/', {'name': 'FLOAT'})

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'subtypes': {'~': {'name': 'FLOAT'}}
            }
        )
