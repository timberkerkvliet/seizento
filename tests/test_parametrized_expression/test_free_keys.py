from unittest import TestCase

from tests.test_client import TestClient


class TestFreeKeys(TestCase):
    def setUp(self) -> None:
        self.test_client = TestClient('localhost')
        self.test_client.put(
            '/schemas/my-seizento/',
            {
                'type': 'MAP',
                'value': {
                    'type': 'STRUCT',
                    'fields': {
                        'a': {'type': 'STRING'},
                        'b': {'type': 'INTEGER'},
                        'nested': {
                            'type': 'STRUCT',
                            'fields': {
                                'p': {'type': 'INTEGER'},
                                'l': {'type': 'ARRAY', 'value': {'type': 'STRING'}}
                            }
                        }
                    }
                }
            }
        )
        self.test_client.put(
            '/schemas/basic-map',
            {'type': 'MAP', 'value': {'type': 'STRING'}}
        )
        self.test_client.put(
            '/expressions/basic-map',
            {'key-1': 'een', 'key-2': 'twee', 'key-3': 'drie'}
        )
        self.test_client.put(
            '/expressions/my-seizento',
            {
                '*parameter': 'tenant_id',
                '*expression': {
                    'a': '{basic-map/{tenant_id}}',
                    'b': 1001,
                    'nested': {
                        'p': 906,
                        'l': ['a', 'list', 'of', 'strings', '{tenant_id}']
                    }
                }
            }
        )

    def test_get_specific_key(self):
        resp = self.test_client.get('/parsed/my-seizento/key-1')
        self.assertEqual(resp, 'een')

    def test_error_on_getting_map(self):
        with self.assertRaises(Exception):
            self.test_client.get('/parsed/my-seizento')
