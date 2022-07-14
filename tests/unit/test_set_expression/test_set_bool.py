from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestBool(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set('/schema/', {'type': 'boolean'})
        self.test_client.set(
            '/expression/',
            True
        )
        response = self.test_client.get('/expression/')
        self.assertEqual(response, True)

    def test_set_wrong_literal(self):
        self.test_client.set('/schema/', {'type': 'boolean'})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/', 9000)
