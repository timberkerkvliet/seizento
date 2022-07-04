from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.test_client import UnitTestClient


class TestDictionary(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        await self.test_client.set('/expression/', {'a': 44, 'p': 99})
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, {'a': 44, 'p': 99})

    async def test_nested_dicts(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'additionalProperties': {'type': 'integer'}
                }
            }
        )
        await self.test_client.set('/expression/', {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})

    async def test_item_evaluation(self):
        await self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        await self.test_client.set('/expression/', {'a': 44, 'p': 99})
        response = await self.test_client.get('/evaluation/p')
        self.assertEqual(response, 99)

    async def test_non_existing_item(self):
        await self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        await self.test_client.set('/expression/', {'a': 44, 'p': 99})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation/pq')

    async def test_empty_object(self):
        await self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        await self.test_client.set('/expression/', {})
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, {})
