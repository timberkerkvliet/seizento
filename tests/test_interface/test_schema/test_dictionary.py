from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, BadRequest
from tests.test_interface.test_client import UnitTestClient


class TestDictionary(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_dict(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'object', 'additionalProperties': {'type': 'string'}})

    async def test_reset_value_type(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )
        await self.test_client.set(
            '/schema/~',
            {'type': 'integer'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response,  {'type': 'object', 'additionalProperties': {'type': 'integer'}})
