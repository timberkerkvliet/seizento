from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetFloatSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_float(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'number'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'number'})

    async def test_set_optional_float(self):
        await self.test_client.set('/schema/', {'type': ['number', 'null']})

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': ['number', 'null']})

    async def test_cannot_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'number'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )

    async def test_cannot_set_placeholder_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'number'}
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )
