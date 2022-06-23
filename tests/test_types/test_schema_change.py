from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


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
