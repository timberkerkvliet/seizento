from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetArray(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_literal(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, 2, 3, 4])
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2, 3, 4])

    async def test_set_empty_array(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [])

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [])

    async def test_reset_index(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1])
        await self.test_client.set('/expression/0', 2)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [2])

    async def test_add_index(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1])
        await self.test_client.set('/expression/1', 2)

        response = await self.test_client.get('/expression/')
        self.assertEqual(response, [1, 2])

    async def test_set_wrong_type(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', 1)

    async def test_set_wrong_value_type(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', ['a', 'b'])

    async def test_set_mixing_types(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', [1, 'b'])

    async def test_set_array_of_structs(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }}
        )

        await self.test_client.set(
            '/expression/',
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

        response = await self.test_client.get('/expression')

        self.assertEqual(
            response,
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

    async def test_set_array_of_dicts(self):
        await self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'string'
                }
            }}
        )

        await self.test_client.set(
            '/expression/',
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )

        response = await self.test_client.get('/expression')

        self.assertEqual(
            response,
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )
