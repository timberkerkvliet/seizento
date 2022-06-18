from unittest import TestCase

from tests.test_client import TestClient


class TestMap(TestCase):
    SCHEMA = {
        'type': 'MAP',
        'value': {
            'type': 'STRUCT',
            'fields': {
                'a': {'type': 'STRING'},
                'b': {'type': 'INTEGER'}
            }
        }
    }

    def setUp(self) -> None:
        self.test_client = TestClient('localhost')
        self.test_client.put('/schemas/my-seizento/', self.SCHEMA)

    def test_get_empty_default(self):
        resp = self.test_client.get('/values/my-seizento')

        self.assertEqual(resp, {})

    def set_literals_for_keys(self):
        self.test_client.put('/expressions/my-seizento/my-key/a', {'a': 'my', 'b': 100})
        self.test_client.put('/expressions/my-seizento/another-key/a', {'a': 'another', 'b': 101})

        resp = self.test_client.get('/expressions/my-seizento/')

        self.assertEqual(
            resp,
            {
                'my-key': {'a': 'my', 'b': 100},
                'another-key': {'a': 'my', 'b': 101}
            }
        )

    def get_value_by_key(self):
        literal = {'a': 'my', 'b': 100}
        self.test_client.put('/expressions/my-seizento/my-key/a', literal)

        resp = self.test_client.get('/values/my-seizento/my-key')

        self.assertEqual(resp, literal)

    def set_generic_expression(self):
        self.test_client.put(
            '/schemas/ref',
            {'type': 'MAP', 'value': {'type': 'STRING'}}
        )
        self.test_client.put(
            '/expressions/ref',
            {'key-1': 'een', 'key-2': 'twee', 'key-3': 'drie'}
        )
        self.test_client.put(
            '/expressions/my-seizento',
            {'*parameter': 'tenant_id', '*expression': 'ref/{tenant_id}'}
        )

        resp = self.test_client.get('/parsed/my-seizento/key-1')
        self.assertEqual(resp, 'een')

    def set_specific_expression(self):
        self.test_client.put(
            '/schemas/ref',
            {'type': 'MAP', 'value': {'type': 'STRING'}}
        )
        self.test_client.put(
            '/expressions/ref',
            {'key-1': 'een', 'key-2': 'twee', 'key-3': 'drie'}
        )
        self.test_client.put(
            '/expressions/my-seizento',
            {
                'key-1': {'*expression': 'ref/key-1'},
                'key-3': {'*expression': 'ref/key-3'}
            }
        )

        resp = self.test_client.get('/parsed/my-seizento')

        self.assertEqual(
            resp,
            {
                'key-1': 'een',
                'key-3': 'drie'
            }
        )
