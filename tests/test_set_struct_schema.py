from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestSetStructSchema(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'subtypes': {
                    'a': {'name': 'STRING'},
                    'b': {'name': 'INTEGER'}
                }
            }
        )

    async def test_reset_struct(self):
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'subtypes': {
                    'c': {'name': 'FLOAT'},
                    'd': {'name': 'BOOLEAN'}
                }
            }
        )
        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'subtypes': {
                    'c': {'name': 'FLOAT'},
                    'd': {'name': 'BOOLEAN'}
                }
            }
        )

    async def test_set_field_type(self):
        await self.test_client.set(
            '/type/a',
            {'name': 'INTEGER'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'subtypes': {
                    'a': {'name': 'INTEGER'},
                    'b': {'name': 'INTEGER'}
                }

            }
        )
