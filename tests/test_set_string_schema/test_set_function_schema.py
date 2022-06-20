from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestSetStringSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_function(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'value_type': {'name': 'INTEGER'}}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'value_type': {'name': 'INTEGER', 'optional': False, 'default_value': None}
            }
        )

    async def test_set_value_type(self):
        await self.test_client.set(
            '/type/',
            {'name': 'FUNCTION', 'value_type': {'name': 'INTEGER'}}
        )
        await self.test_client.set(
            '/type/~/',
            {'name': 'FLOAT'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'FUNCTION',
                'value_type': {'name': 'FLOAT', 'optional': False, 'default_value': None}
            }
        )
