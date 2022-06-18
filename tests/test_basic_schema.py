from unittest import TestCase

from tests.test_client import TestClient


class TestBasicSchema(TestCase):
    SCHEMA = {
        'type': 'STRING',
        'default_value': 'hey'
    }

    def setUp(self) -> None:
        self.test_client = TestClient('localhost')
        self.test_client.put('/schemas/my-seizento/', self.SCHEMA)

    def test_get_schema(self):
        response = self.test_client.get('/schemas/my-seizento/')

        self.assertEqual(response['type'], 'STRING')

    def test_get_default(self):
        response = self.test_client.get('/parsed/my-seizento/')

        self.assertEqual(response, 'hey')

    def test_set_literal(self):
        self.test_client.put('/expressions/my-seizento/', 'some value')

        response = self.test_client.get('/values/my-seizento/')

        self.assertEqual(response, 'some value')

    def test_set_expression(self):
        self.test_client.put('/schemas/basic', {'type': 'STRING', 'default_value': 'basic'})
        self.test_client.put('/expressions/my-seizento', '/basic')

        resp = self.test_client.get('/parsed/my-seizento')

        self.assertEqual(resp, 'basic')


