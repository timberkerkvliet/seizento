from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestInteger(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set('/schema/test/', {'type': 'integer'})
        self.test_client.set(
            '/expression/test/',
            -7
        )
        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, -7)

    def test_set_wrong_literal(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', 8.77)
