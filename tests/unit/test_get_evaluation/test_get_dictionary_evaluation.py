from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetDictionaryEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/expression/', {'a': 44, 'p': 99})
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, {'a': 44, 'p': 99})

    async def test_nested_dicts(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'additionalProperties': {'type': 'integer'}
                }
            }
        )
        self.test_client.set('/expression/', {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})

    async def test_item_evaluation(self):
        self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/expression/', {'a': 44, 'p': 99})
        response = self.test_client.get('/evaluation/p')
        self.assertEqual(response, 99)

    async def test_non_existing_item(self):
        self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/expression/', {'a': 44, 'p': 99})

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation/pq')

    async def test_empty_object(self):
        self.test_client.set('/schema/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/expression/', {})
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, {})
