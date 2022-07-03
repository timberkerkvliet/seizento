from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.test_interface.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_not_found_before_set(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'integer'}}
            }
        )

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation/')
