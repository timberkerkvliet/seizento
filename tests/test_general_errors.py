from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, BadRequest
from tests.test_client import UnitTestClient


class TestGeneralErrors(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_non_existing(self):
        with self.assertRaises(NotFound):
            await self.test_client.set(
                '/schema/a', {'name': 'INTEGER'}
            )

    async def test_rubbish_path(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                'plfo//dsf', {}
            )

    async def test_non_existing_root_type(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                '/hoi-daar-allemaal', {}
            )

    async def test_set_empty_type_data(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set(
                '/type', {}
            )
