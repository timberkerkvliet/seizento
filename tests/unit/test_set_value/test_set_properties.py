from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetProperties(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_one_free_property_can_be_set(self):
        self.test_client.set('schema/test', {'properties': {'a': {}}, 'additionalProperties': False})

        try:
            self.test_client.set('value/test', {'a': ['everything', 'I', 'want']})
        except Forbidden:
            self.fail()

    def test_set_no_additional_properties(self):
        self.test_client.set('schema/test', {'additionalProperties': False})

        with self.assertRaises(Forbidden):
            self.test_client.set('value/test', {'a': 8})

    def test_set_one_free_property_something_else_cannot_be_set(self):
        self.test_client.set('schema/test', {'properties': {'a': {}}, 'additionalProperties': False})

        with self.assertRaises(Forbidden):
            self.test_client.set('value/test', {'b': 'else'})
