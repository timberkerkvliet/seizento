from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetBoolEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_true(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})
        await self.test_client.set('/expression/', True)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, True)

    async def test_set_false(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})
        await self.test_client.set('/expression/', False)

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, False)

    async def test_not_set(self):
        await self.test_client.set('/schema/', {'type': 'boolean'})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation')
