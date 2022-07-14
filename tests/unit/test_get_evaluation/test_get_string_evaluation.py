from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetStringEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal_with_escaped_brackets(self):
        self.test_client.set('/schema/', {'type': 'string'})
        self.test_client.set(
            '/expression/',
            'a literal {{ string'
        )
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal { string')

    def test_set_and_get_literal_with_double_escaped_brackets(self):
        self.test_client.set('/schema/', {'type': 'string'})
        self.test_client.set(
            '/expression/',
            '{{a}}'
        )
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, '{a}')

    def test_set_and_evaluate_literal(self):
        self.test_client.set('/schema/', {'type': 'string'})
        self.test_client.set('/expression/', 'a literal string')

        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    def test_missing_value(self):
        self.test_client.set('/schema/', {'type': 'string'})

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation')
