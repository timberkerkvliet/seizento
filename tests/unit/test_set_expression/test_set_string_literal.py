from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetStringLiteral(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_literal(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        self.test_client.set('/expression/test/', 'a literal string')
        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, 'a literal string')

    def test_set_null(self):
        self.test_client.set('/schema/test/', {'type': ['string', 'null']})
        self.test_client.set('/expression/test/', None)

        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, None)

    def test_cannot_set_null_if_non_optional(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', None)

    def test_set_wrong_literal(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', 9000)
