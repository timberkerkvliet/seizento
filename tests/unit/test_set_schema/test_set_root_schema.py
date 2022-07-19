from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetRootSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_integer(self):
        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/schema/',
                {'type': 'integer'}
            )

    def test_set_object(self):
        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/schema/',
                {'type': 'object'}
            )
