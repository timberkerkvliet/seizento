from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetBoolSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_bool(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'boolean'})

    async def test_set_optional_bool(self):
        await self.test_client.set('/schema/', {'type': ['boolean', 'null']})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': ['boolean', 'null']})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'boolean'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'boolean'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )
