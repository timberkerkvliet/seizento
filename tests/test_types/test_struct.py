from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_struct(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'STRUCT',
                'fields': {
                    'a': {'type': 'STRING'},
                    'b': {'type': 'INTEGER'}
                }
            }
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'STRUCT',
                'fields': {
                    'a': {'type': 'STRING'},
                    'b': {'type': 'INTEGER'}
                }
            }
        )

    async def test_reset_struct(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'STRUCT',
                'fields': {'a': {'type': 'FLOAT'}}
            }
        )
        await self.test_client.set(
            '/schema/',
            {
                'type': 'STRUCT',
                'fields': {'b': {'type': 'INTEGER'}}
            }
        )
        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'STRUCT',
                'fields': {
                    'b': {'type': 'INTEGER'}
                }
            }
        )

    async def test_set_field_type(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'STRUCT',
                'fields': {'a': {'type': 'FLOAT'}, 'b': {'type': 'STRING'}}
            }
        )
        await self.test_client.set(
            '/schema/a',
            {'type': 'INTEGER'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'STRUCT',
                'fields': {
                    'a': {'type': 'INTEGER'},
                    'b': {'type': 'STRING'}
                }

            }
        )

    async def test_add_field_types(self):
        await self.test_client.set('schema/', {'type': 'STRUCT'})
        await self.test_client.set(
            '/schema/c',
            {'type': 'INTEGER'}
        )
        await self.test_client.set(
            '/schema/d',
            {'type': 'STRING'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'STRUCT',
                'fields': {
                    'c': {'type': 'INTEGER'},
                    'd': {'type': 'STRING'}
                }

            }
        )

    async def test_delete_field_type(self):
        await self.test_client.set('schema/', {'type': 'STRUCT', 'fields': {'a': {'type': 'STRING'}}})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'STRUCT'}
        )

    async def test_non_existing_field_type(self):
        await self.test_client.set('/schema', {'type': 'STRUCT'})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'STRUCT'}
        )
