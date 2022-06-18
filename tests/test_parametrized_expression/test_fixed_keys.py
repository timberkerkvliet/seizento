from unittest import TestCase

from tests.test_client import TestClient


class TestFixedKeys(TestCase):
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
                        'b': {'type': 'INTEGER'}
                    }
                }
            }
        )
        self.test_client.put(
            '/schemas/basic-map',
            {'type': 'MAP', 'value': {'type': 'STRING'}}
        )
        self.test_client.put(
            '/values/basic-map',
            {'key-1': 'een', 'key-2': 'twee', 'key-3': 'drie'}
        )
        self.test_client.put(
            '/values/my-seizento',
            {'*parameters': ['tenant_id'], '*expression': 'ref/{tenant_id}', '*keys': ['key-1', 'key-2']}
        )

    def test_get_specific_key(self):
        resp = self.test_client.get('/values/my-seizento/key-1')
        self.assertEqual(resp, 'een')

    def test_get_map(self):
        resp = self.test_client.get('/parsed/my-seizento')
        self.assertDictEqual(resp, {'key-1': 'een', 'key-2': 'twee'})
