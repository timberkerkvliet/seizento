from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSchemaChange(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_change(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'integer'})

    async def test_change_to_integer_after_string_expression_has_set(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set('/expression/', 'hey')

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema/', {'type': 'integer'})

    async def test_allowed_change(self):
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
