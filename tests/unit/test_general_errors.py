from unittest import TestCase

from seizento.controllers.exceptions import BadRequest
from tests.unit.unit_test_client import UnitTestClient


class TestGeneralErrors(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_when_getting_nonsensical_resource_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            self.test_client.get('plfo//dsf')

    def test_when_getting_non_existing_base_type_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            self.test_client.get('/hoi-daar-allemaal')
