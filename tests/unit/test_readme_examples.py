from unittest import IsolatedAsyncioTestCase

from tests.unit.unit_test_client import UnitTestClient


class TestReadmeExample(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_first_case(self):
        await self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'properties': {
                    'products': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'on_stock': {'type': 'boolean'}
                            }
                        }
                    },
                    'stock': {
                        'type': 'object',
                        'additionalProperties':  {'type': 'boolean'}
                    }
                }

            }
        )

        await self.test_client.set(
            '/expression/',
            {
                'products': [
                    {
                        'id': 1,
                        'name': 'Boring product',
                        'on_stock': True
                    },
                    {
                        'id': 2,
                        'name': 'Fancy product',
                        'on_stock': False
                    }
                ],
                'stock': {
                    '*parameter': 'k',
                    '*property': '{products/<k>/name}',
                    '*value': '{products/<k>/on_stock}'
                }
            }
        )

        result = await self.test_client.get('/evaluation/stock')

        self.assertDictEqual(
            result,
            {'Boring product': True, 'Fancy product': False}
        )
