from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetIntegerSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_integer(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'integer'})

    async def test_set_optional_integer(self):
        await self.test_client.set('/schema/', {'type': ['integer', 'null']})

        response = await self.test_client.get('/schema/')
        self.assertEqual(set(response['type']), {'integer', 'null'})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        try:
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    async def test_can_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        try:
            await self.test_client.set(
                '/schema/~items',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    async def test_can_set_integer_if_string_is_set(self):
        await self.test_client.set('/schema/', {'type': 'string'})

        try:
            await self.test_client.set('/schema/', {'type': 'integer'})
        except Forbidden:
            self.fail()

    async def test_change_to_integer_after_string_expression_has_set(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set('/expression/', 'hey')

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema/', {'type': 'integer'})

    async def test_set_struct_field_to_integer(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}, 'b': {'type': 'string'}}
            }
        )

        await self.test_client.set('/schema/a', {'type': 'integer'})

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
