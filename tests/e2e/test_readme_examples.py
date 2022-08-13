from tests.e2e.e2e_test_client import E2ETestClient
from tests.unit.test_readme_examples import TestReadmeExample


class E2ETestReadmeExample(TestReadmeExample):
    def setUp(self) -> None:
        self.test_client = E2ETestClient()
        self.test_client.__enter__()

    def tearDown(self) -> None:
        self.test_client.__exit__()

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

        self.test_client.set('/value/products', literal)

        result = self.test_client.get('/value/products')

        self.assertEqual(literal, result)
