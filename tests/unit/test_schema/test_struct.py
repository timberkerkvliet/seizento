from unittest import IsolatedAsyncioTestCase

from tests.unit.unit_test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_When_struct_schema_is_set_Then_get_schema_back(self):
        schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'string'},
                'b': {'type': 'integer'}
            }
        }
        await self.test_client.set('/schema/', schema)

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, schema)

    async def test_Given_a_struct_schema_when_schema_is_reset_Then_get_new_schema_back(self):
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

    async def test_Given_a_struct_schema_when_field_schema_is_reset_Then_get_changed_schema_back(self):
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

    async def test_Given_an_empty_struct_When_add_fields_Then_get_added_fields_back(self):
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

    async def test_Given_a_struct_schema_When_delete_field_Then_get_schema_without_field_back(self):
        await self.test_client.set('schema/', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )

    async def test_Given_an_empty_struct_schema_When_nonexisting_field_deleted_Then_get_same_schema_back(self):
        await self.test_client.set('/schema', {'type': 'object'})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )
