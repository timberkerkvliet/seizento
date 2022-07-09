from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_null(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'null'}
        )

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'null'})
