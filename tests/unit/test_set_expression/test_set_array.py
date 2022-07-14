from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_literal(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1, 2, 3, 4])
        response = self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])

    async def test_set_empty_array(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [])

        response = self.test_client.get('/expression/')
        self.assertEqual(response, [])

    async def test_reset_index(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1])
        self.test_client.set('/expression/0', 2)

        response = self.test_client.get('/expression/')
        self.assertEqual(response, [2])

    async def test_add_index(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1])
        self.test_client.set('/expression/1', 2)

        response = self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2])

    async def test_set_wrong_type(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/', 1)

    async def test_set_wrong_value_type(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/', ['a', 'b'])

    async def test_set_mixing_types(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/', [1, 'b'])

    async def test_set_array_of_structs(self):
        self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }}
        )

        self.test_client.set(
            '/expression/',
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

        response = self.test_client.get('/expression')

        self.assertEqual(
            response,
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

    async def test_set_array_of_dicts(self):
        self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'string'
                }
            }}
        )

        self.test_client.set(
            '/expression/',
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )

        response = self.test_client.get('/expression')

        self.assertEqual(
            response,
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )
