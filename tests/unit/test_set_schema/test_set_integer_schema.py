from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetIntegerSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_string(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'integer'})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'integer'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )

    async def test_can_set_integer_if_string_is_set(self):
        await self.test_client.set('/schema/', {'type': 'string'})

        try:
            await self.test_client.set('/schema/', {'type': 'integer'})
        except Forbidden:
            self.fail()

