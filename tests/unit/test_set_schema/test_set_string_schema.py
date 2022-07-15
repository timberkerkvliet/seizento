from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetStringSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_string(self):
        self.test_client.set('/schema/test/', {'type': 'string'})

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'string'})

    def test_set_optional_string(self):
        self.test_client.set('/schema/test/', {'type': ['string', 'null']})

        response = self.test_client.get('/schema/test/')
        self.assertEqual(set(response['type']), {'string', 'null'})

    def test_set_optional_string_after_string_literal_has_been_set(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        self.test_client.set('/expression/test', 'my string')

        try:
            self.test_client.set('/schema/test', {'type': ['string', 'null']})
        except Forbidden:
            self.fail()

    def test_set_string_after_null_has_been_set(self):
        self.test_client.set('/schema/test/', {'type': ['null', 'string']})
        self.test_client.set('/expression/test', None)

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/test', {'type': 'string'})

    def test_set_string_after_string_literal_has_been_set(self):
        self.test_client.set('/schema/test/', {'type': ['null', 'string']})
        self.test_client.set('/expression/test', 'a string')

        try:
            self.test_client.set('/schema/test', {'type': 'string'})
        except Forbidden:
            self.fail()

    def test_can_set_child(self):
        self.test_client.set('/schema/test/', {'type': 'string'})

        try:
            self.test_client.set(
                '/schema/test/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_can_set_placeholder_child(self):
        self.test_client.set('/schema/test/', {'type': 'string'})

        try:
            self.test_client.set(
                '/schema/test/~',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()
