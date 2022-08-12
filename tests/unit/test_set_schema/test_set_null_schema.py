from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetNullSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_null(self):
        self.test_client.set('/schema/test/', {'type': 'null'})

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'null'})

    def test_set_null_schema_if_null_is_set(self):
        self.test_client.set('/schema/test/', {'type': ['null', 'string']})
        self.test_client.set('/value/test/', None)

        try:
            self.test_client.get('/schema/test/')
        except Forbidden:
            self.fail()

    def test_set_null_schema_if_literal_string_is_set(self):
        self.test_client.set('/schema/test/', {'type': ['null', 'string']})
        self.test_client.set('/value/test/', 'a string')

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/test/', {'type': 'null'})

    def test_set_null_schema_if_object_schema_is_set(self):
        self.test_client.set('/schema/test/', {'type': 'object'})
        self.test_client.set('/value/test/', {})

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/test/', {'type': 'null'})

    def test_set_null_schema_if_array_schema_is_set(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'string'}})
        self.test_client.set('/value/test/', [])

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/test/', {'type': 'null'})
