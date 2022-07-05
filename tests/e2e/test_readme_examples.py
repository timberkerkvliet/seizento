from unittest import IsolatedAsyncioTestCase

from tests.e2e.e2e_test_client import E2ETestClient


class TestReadmeExample(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = E2ETestClient()
        self.test_client.__enter__()

    def tearDown(self) -> None:
        self.test_client.__exit__()

    async def test_products_example_set_literals(self):
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
                    }
                }

            }
        )

        literal = {
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
                ]
            }

        self.test_client.set('/expression/', literal)

        result = self.test_client.get('/evaluation')

        self.assertDictEqual(literal, result)

    async def test_products_example_set_projection(self):
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
                    }
                }

            }
        )
        self.test_client.set(
            '/schema/stock',
            {
                "type": "object",
                "additionalProperties": {
                    {"type": "boolean"}
                }
            }
        )

        self.test_client.set(
            '/expression/stock',
            {
                "*parameter": "k",
                "*property": "{products/<k>/name}",
                "*value": "{products/<k>/on_stock}"
            }
        )

        result = self.test_client.get('/evaluation/stock')

        self.assertDictEqual(
            {
                "Boring product": True,
                "Fancy product": False
            },
            result
        )
