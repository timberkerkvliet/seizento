from unittest import TestCase

from tests.test_client import TestClient


class TestArrayOfStructs(TestCase):
    SCHEMA = {
        'type': 'ARRAY',
        'elements': {
            'type': 'STRUCT',
            'fields': {
                'a-field': {'type': 'STRING'},
                'another-field': {'type': 'INTEGER'}
            }
        }
    }

    def setUp(self) -> None:
        self.test_client = TestClient('localhost')
        self.test_client.put('/schemas/my-seizento/', self.SCHEMA)

    def test_get_empty_list_as_default(self):
        response = self.test_client.get('/parsed/my-seizento/')

        self.assertEqual(response, [])

    def test_set_literal(self):
        literal = [
            {
                'a-field': 'a value',
                'another-field': 1988
            },
            {
                'a-field': 'jazz',
                'another-field': 2014
            }
        ]
        self.test_client.put('/literals/my-seizento/', literal)

        response = self.test_client.get('/parsed/my-seizento/')

        self.assertEqual(response, literal)

    def test_set_object_reference(self):
        self.test_client.put(
            '/schemas/ref',
            {
                'type': 'STRUCT',
                'fields': {
                    'a-field': {'type': 'STRING', 'default_value': 'X'},
                    'another-field': {'type': 'INTEGER', 'default_value': 4}
                }
            }
        )

        self.test_client.put(
            '/expressions/my-seizento',
            [
                {
                    'a-field': 'hoi',
                    'another-field': 1988
                },
                {
                    'a-field': {'*reference': 'ref/a-field'},
                    'another-field': {'*reference': 'ref/another-field'}
                },
                {
                    '*reference': 'ref'
                }
            ]
        )

        response = self.test_client.get('/values/my-seizento/')

        self.assertEqual(
            response,
            [
                {'a-field': 'hoi', 'another-field': 1988},
                {'a-field': 'X', 'another-field': 4},
                {'a-field': 'X', 'another-field': 4}
            ]
        )