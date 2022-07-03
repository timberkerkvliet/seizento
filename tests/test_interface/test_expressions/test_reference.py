from unittest import IsolatedAsyncioTestCase, skip

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.test_interface.test_client import UnitTestClient


class TestReference(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_reference(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', [1, '{/0}'])

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1])

    async def test_non_existing_key(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        await self.test_client.set('/expression/', ['{/1}'])

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation/')

    async def test_reference_with_wrong_type(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        await self.test_client.set('/expression', {'a': 5})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/b', '{/a}')

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

    async def test_cycle_of_three(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        await self.test_client.set('/expression/', ['{/1}', '{/2}'])

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/2', '{/0}')

    async def test_self_reference(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression', ['{/0}'])

    async def test_self_reference_did_not_change_anything(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        await self.test_client.set('/expression', [1])

        try:
            await self.test_client.set('/expression', ['{/0}'])
        except Forbidden:
            pass

        response = await self.test_client.get('/expression')

        self.assertEqual(response, [1])
