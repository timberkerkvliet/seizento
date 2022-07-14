from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetNullSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_null(self):
        self.test_client.set('/schema/', {'type': 'null'})

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'null'})

    def test_set_null_schema_if_null_is_set(self):
        self.test_client.set('/schema/', {'type': ['null', 'string']})
        self.test_client.set('/expression/', None)

        try:
            self.test_client.get('/schema/')
        except Forbidden:
            self.fail()

    def test_set_null_schema_if_literal_string_is_set(self):
        self.test_client.set('/schema/', {'type': ['null', 'string']})
        self.test_client.set('/expression/', 'a string')

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/', {'type': 'null'})

    def test_set_null_schema_if_object_schema_is_set(self):
        self.test_client.set('/schema/', {'type': 'object'})
        self.test_client.set('/expression/', {})

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/', {'type': 'null'})

    def test_set_null_schema_if_array_schema_is_set(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'string'}})
        self.test_client.set('/expression/', [])

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/', {'type': 'null'})
