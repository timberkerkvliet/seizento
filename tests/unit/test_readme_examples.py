from unittest import TestCase

from tests.unit.unit_test_client import UnitTestClient


class TestReadmeExample(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_products_example_set_literals(self):
        self.test_client.set(
            '/schema/products',
            {
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
        )

        literal = [
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

        self.test_client.set('/expression/products', literal)

        result = self.test_client.get('/evaluation/products')

        self.assertEqual(literal, result)

    def test_products_example_set_projection(self):
        self.test_client.set(
            '/schema/products',
            {
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
        )

        self.test_client.set(
            '/expression/products',
            [
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
        )

        self.test_client.set(
            '/schema/stock',
            {
                "type": "object",
                "additionalProperties": {"type": "boolean"}
            }
        )

        self.test_client.set(
            '/expression/stock',
            {
                "*parameter": "k",
                "*property": "{/products/<k>/name}",
                "*value": "{/products/<k>/on_stock}"
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
