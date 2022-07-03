from unittest import IsolatedAsyncioTestCase

from tests.test_interface.test_client import UnitTestClient


class TestParametrizedDictionary(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_with_fixed_object(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        )
        await self.test_client.set(
            '/expression/',
            {
                'fixed': {'een': 1, 'twee': 2, 'drie': 3},
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/fixed/<k>}'
                }
            }
        )
        response = await self.test_client.get('/evaluation/projection')
        self.assertEqual(response, {'een': 1, 'twee': 2, 'drie': 3})

    async def test_with_fixed_array(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        )
        await self.test_client.set(
            '/expression/',
            {
                'fixed': [1, 2, 3],
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/fixed/<k>}'
                }
            }
        )
        response = await self.test_client.get('/evaluation/projection')
        self.assertEqual(response, {'0': 1, '1': 2, '2': 3})
