from unittest import IsolatedAsyncioTestCase

from tests.test_interface.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_struct(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'string'},
                    'b': {'type': 'integer'}
                }
            }
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'string'},
                    'b': {'type': 'integer'}
                }
            }
        )

    async def test_reset_struct(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}}
            }
        )
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'b': {'type': 'integer'}}
            }
        )
        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'b': {'type': 'integer'}
                }
            }
        )

    async def test_set_field_type(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}, 'b': {'type': 'string'}}
            }
        )
        await self.test_client.set(
            '/schema/a',
            {'type': 'integer'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }

            }
        )

    async def test_add_field_types(self):
        await self.test_client.set('schema/', {'type': 'object'})
        await self.test_client.set(
            '/schema/c',
            {'type': 'integer'}
        )
        await self.test_client.set(
            '/schema/d',
            {'type': 'string'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'c': {'type': 'integer'},
                    'd': {'type': 'string'}
                }

            }
        )

    async def test_delete_field_type(self):
        await self.test_client.set('schema/', {'type': 'object', 'properties': {'a': {'type': 'string'}}})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )

    async def test_non_existing_field_type(self):
        await self.test_client.set('/schema', {'type': 'object'})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )
