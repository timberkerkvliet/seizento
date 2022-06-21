from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.test_client import UnitTestClient


class TestEmpty(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_non_existing(self):
        with self.assertRaises(NotFound):
            await self.test_client.set(
                '/type/a', {'name': 'INTEGER'}
            )
