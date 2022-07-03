from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.test_interface.test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
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
        await self.test_client.set(
            '/expression/',
            {'a': 1001, 'b': 'nachten'}
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, {'a': 1001, 'b': 'nachten'})

    async def test_set_partially(self):
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
        await self.test_client.set(
            '/expression/',
            {'a': 1001}
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, {'a': 1001})

    async def test_empty(self):
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
        await self.test_client.set('/expression/', {})
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, {})

    async def test_get_field_expression(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'}
                }
            }
        )
        await self.test_client.set('/expression/', {'a': 9})

        response = await self.test_client.get('expression/a')

        self.assertEqual(response, 9)

    async def test_nested_struct(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'object',
                        'properties': {
                            'b': {'type': 'integer'}
                        }
                    }
                }
            }
        )
        await self.test_client.set('/expression', {'a': {'b': 99}})

        response = await self.test_client.get('/expression/a/b')

        self.assertEqual(response, 99)
