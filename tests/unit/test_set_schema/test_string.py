from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_string(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'string'})

    async def test_set_optional_string(self):
        await self.test_client.set(
            '/schema/',
            {'type': ['string', 'null']}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': ['string', 'null']})

    async def test_set_optional_string_after_string_literal_has_been_set(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set('/expression', 'my string')

        try:
            await self.test_client.set('/schema', {'type': ['string', 'null']})
        except Forbidden:
            self.fail()

    async def test_set_string_after_null_has_been_set(self):
        await self.test_client.set('/schema/', {'type': ['null', 'string']})
        await self.test_client.set('/expression', None)

        with self.assertRaises(Forbidden):
            await self.test_client.set('/schema', {'type': 'string'})

    async def test_set_string_after_string_literal_has_been_set(self):
        await self.test_client.set('/schema/', {'type': ['null', 'string']})
        await self.test_client.set('/expression', 'a string')

        try:
            await self.test_client.set('/schema', {'type': 'string'})
        except Forbidden:
            self.fail()

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'string'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )
