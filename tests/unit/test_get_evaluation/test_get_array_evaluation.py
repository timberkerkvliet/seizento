from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetArrayEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, 2, 3, 4])
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 2, 3, 4])

    async def test_nested_arrays(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'integer'}}}
        )
        await self.test_client.set('/expression/', [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]])
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]])

    async def test_item_evaluation(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, 2, 3, 4])
        response = await self.test_client.get('/evaluation/1')
        self.assertEqual(response, 2)

    async def test_non_existing_item(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, 2, 3, 4])
        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation/4')

    async def test_empty_array(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [])
        response = await self.test_client.get('/evaluation/')

        self.assertEqual(response, [])
