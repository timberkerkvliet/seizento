from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_struct(self):
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'children': {
                    'a': {'name': 'STRING'},
                    'b': {'name': 'INTEGER'}
                }
            }
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'children': {
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
                'children': {'a': {'name': 'FLOAT'}}
            }
        )
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'children': {'b': {'name': 'INTEGER'}}
            }
        )
        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'children': {
                    'b': {'name': 'INTEGER'}
                }
            }
        )

    async def test_set_field_type(self):
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'children': {'a': {'name': 'FLOAT'}, 'b': {'name': 'STRING'}}
            }
        )
        await self.test_client.set(
            '/type/a',
            {'name': 'INTEGER'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'children': {
                    'a': {'name': 'INTEGER'},
                    'b': {'name': 'STRING'}
                }

            }
        )

    async def test_add_field_types(self):
        await self.test_client.set('type/', {'name': 'STRUCT'})
        await self.test_client.set(
            '/type/c',
            {'name': 'INTEGER'}
        )
        await self.test_client.set(
            '/type/d',
            {'name': 'STRING'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {
                'name': 'STRUCT',
                'children': {
                    'c': {'name': 'INTEGER'},
                    'd': {'name': 'STRING'}
                }

            }
        )

    async def test_delete_field_type(self):
        await self.test_client.set('type/', {'name': 'STRUCT', 'children': {'a': {'name': 'STRING'}}})
        await self.test_client.delete('/type/a')

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {'name': 'STRUCT'}
        )

    async def test_non_existing_field_type(self):
        await self.test_client.set('/type', {'name': 'STRUCT'})
        await self.test_client.delete('/type/a')

        response = await self.test_client.get('/type/')
        self.assertDictEqual(
            response,
            {'name': 'STRUCT'}
        )
