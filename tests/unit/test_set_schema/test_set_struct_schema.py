from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_struct_schema_is_persisted(self):
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

    async def test_reset_struct_schema_is_persisted(self):
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

    async def test_adding_fields(self):
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

    async def test_extending_fields(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}}
        )
        await self.test_client.set('/expression/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            }
        }

        await self.test_client.set('/schema/', new_schema)

        response = await self.test_client.get('/schema')

        self.assertDictEqual(response, new_schema)

    async def test_set_field_name_with_special_chars(self):
        try:
            await self.test_client.set(
                '/schema',
                {'type': 'object', 'properties': {'^ (&@a9.?$#/{é': {'type': 'string'}}}
            )
        except BadRequest:
            self.fail()

    async def test_set_struct_from_dict(self):
        await self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        await self.test_client.set('/expression', {'a': 'a'})

        try:
            await self.test_client.set('/schema', {'type': 'object', 'properties': {'a': {'type': 'string'}}})
        except Forbidden:
            self.fail()

    async def test_set_struct_from_dict_with_nested(self):
        await self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'string'},
                        'b': {'type': 'integer'}
                    }
                }
            }
        )
        await self.test_client.set('/expression', {'Ti': {'a': 'string'}})

        try:
            await self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'string'},
                            'c': {'type': 'integer'}
                        }
                    }
                }
            )
        except Forbidden:
            self.fail()

    async def test_cannot_set_struct_from_dict_with_nested(self):
        await self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'string'},
                        'b': {'type': 'integer'}
                    }
                }
            }
        )
        await self.test_client.set('/expression', {'Ti': {'a': 'string'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema',
                {
                    'type': 'object',
                    'additionalProperties': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'integer'},
                            'c': {'type': 'integer'}
                        }
                    }
                }
            )

    async def test_set_struct_from_dict_if_empty_is_set(self):
        await self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        await self.test_client.set('/expression', {})

        try:
            await self.test_client.set('/schema', {'type': 'object', 'properties': {'a': {'type': 'string'}}})
        except Forbidden:
            self.fail()

    async def test_set_struct_from_non_matching_dict(self):
        await self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        await self.test_client.set('/expression', {'b': 'b'})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema', {'type': 'object', 'properties': {'a': {'type': 'string'}}})
