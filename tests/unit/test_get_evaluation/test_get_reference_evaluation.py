from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetReferenceEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_reference(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, '{/0}'])

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1])

    async def test_non_existing_key(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/', ['{/1}'])

    async def test_object_reference(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'object', 'properties': {'x': {'type': 'string'}}},
                    'b': {'type': 'object', 'properties': {'x': {'type': 'string'}}}
                }
            }
        )
        await self.test_client.set(
            '/expression',
            {
                'a': {'x': 'copy this'},
                'b': '{/a}'
            }
        )

        response = await self.test_client.get('/evaluation/')

        self.assertDictEqual(
            response,
            {
                'a': {'x': 'copy this'},
                'b': {'x': 'copy this'}
             }
        )

    async def test_double_reference(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1])

        await self.test_client.set('/expression/1', '{/0}')
        await self.test_client.set('/expression/2', '{/1}')

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1, 1])
