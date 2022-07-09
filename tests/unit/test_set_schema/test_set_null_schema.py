from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetNullSchema(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_null(self):
        await self.test_client.set('/schema/', {'type': 'null'})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'null'})

    async def test_set_null_schema_if_null_is_set(self):
        await self.test_client.set('/schema/', {'type': ['null', 'string']})
        await self.test_client.set('/expression/', None)

        try:
            await self.test_client.get('/schema/')
        except Forbidden:
            self.fail()

    async def test_set_null_schema_if_literal_string_is_set(self):
        await self.test_client.set('/schema/', {'type': ['null', 'string']})
        await self.test_client.set('/expression/', 'a string')

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema/', {'type': 'null'})

    async def test_set_null_schema_if_object_schema_is_set(self):
        await self.test_client.set('/schema/', {'type': 'object'})
        await self.test_client.set('/expression/', {})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema/', {'type': 'null'})

    async def test_set_null_schema_if_array_schema_is_set(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'string'}})
        await self.test_client.set('/expression/', [])

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema/', {'type': 'null'})
