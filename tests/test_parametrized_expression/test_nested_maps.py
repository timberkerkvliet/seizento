from unittest import TestCase

from tests.test_client import TestClient


class TestNestedFunctions(TestCase):
    def setUp(self) -> None:
        self.test_client = TestClient('localhost')
        self.test_client.put(
            '/schemas/my-seizento/',
            {
                'type': 'FUNCTION',
                'value': {
                    'type': 'FUNCTION',
                    'value': {
                        'type': 'STRING'
                    }
                }
            }
        )
        self.test_client.put(
            '/schemas/basic-map',
            {'type': 'FUNCTION', 'value': {'type': 'FUNCTION', 'value': {'type': 'INTEGER'}}}
        )
        self.test_client.put(
            '/values/basic-map',
            {
                'key-1': {'a': 1},
                'key-2': {'a': 2, 'b': 4},
                'key-3': {'a': 3, 'b': 6, 'c': 7}
            }
        )
        self.test_client.put(
            '/templates/my-seizento',
            {'key': {'letter': '{basic-map/[key]/[letter]}'}}
        )

    def test_get_specific_key(self):
        resp = self.test_client.get('/values/my-seizento/key-1')
        self.assertEqual(resp, 'een')

    def test_error_on_getting_map(self):
        with self.assertRaises(Exception):
            self.test_client.get('/parsed/my-seizento')

    f'hella {{ {hoi/[key]}'