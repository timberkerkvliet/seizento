from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestArray(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_array(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {'type': 'string'}}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'array', 'items': {'type': 'string'}})

    async def test_without_items(self):
        try:
            await self.test_client.set('/schema/', {'type': 'array'})
        except BadRequest:
            self.fail()

    async def test_reset_value_type(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {'type': 'string'}}
        )
        await self.test_client.set('/schema/~items', {'type': 'integer'})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response,  {'type': 'array', 'items': {'type': 'integer'}})

    async def test_cannot_remove_value_type(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {'type': 'string'}}
        )
        try:
            await self.test_client.delete('/schema/~items',)
        except Forbidden:
            self.fail()
