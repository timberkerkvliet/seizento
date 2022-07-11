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
        self.assertEqual(set(response['type']), {'boolean', 'null'})

    async def test_can_set_child(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'boolean'}
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
            {'type': 'boolean'}
        )

        try:
            await self.test_client.set(
                '/schema/~items',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()