from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.test_interface.test_client import UnitTestClient


class TestBool(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal_with_escaped_brackets(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})
        await self.test_client.set('/expression/', True)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, True)
