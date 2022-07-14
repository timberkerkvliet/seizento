from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetStringSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_string(self):
        self.test_client.set('/schema/', {'type': 'string'})

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'string'})

    def test_set_optional_string(self):
        self.test_client.set('/schema/', {'type': ['string', 'null']})

        response = self.test_client.get('/schema/')
        self.assertEqual(set(response['type']), {'string', 'null'})

    def test_set_optional_string_after_string_literal_has_been_set(self):
        self.test_client.set('/schema/', {'type': 'string'})
        self.test_client.set('/expression', 'my string')

        try:
            self.test_client.set('/schema', {'type': ['string', 'null']})
        except Forbidden:
            self.fail()

    def test_set_string_after_null_has_been_set(self):
        self.test_client.set('/schema/', {'type': ['null', 'string']})
        self.test_client.set('/expression', None)

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema', {'type': 'string'})

    def test_set_string_after_string_literal_has_been_set(self):
        self.test_client.set('/schema/', {'type': ['null', 'string']})
        self.test_client.set('/expression', 'a string')

        try:
            self.test_client.set('/schema', {'type': 'string'})
        except Forbidden:
            self.fail()

    def test_can_set_child(self):
        self.test_client.set('/schema/', {'type': 'string'})

        try:
            self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_can_set_placeholder_child(self):
        self.test_client.set('/schema/', {'type': 'string'})

        try:
            self.test_client.set(
                '/schema/~',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()
