from unittest import IsolatedAsyncioTestCase

from tests.e2e.e2e_test_client import E2ETestClient
from tests.unit.unit_test_client import UnitTestClient


class TestReadmeExample(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = E2ETestClient()
        self.test_client.__enter__()

    def tearDown(self) -> None:
        self.test_client.__exit__()

    async def test_first_case(self):
        self.test_client.set(
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

        self.test_client.set(
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

        result = self.test_client.get('/evaluation/stock')

        self.assertDictEqual(
            result,
            {'Boring product': True, 'Fancy product': False}
        )
