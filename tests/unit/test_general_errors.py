from unittest import TestCase

from seizento.controllers.exceptions import NotFound, BadRequest, MethodNotAllowed, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGeneralErrors(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_when_setting_schema_with_no_paren_then_raise_not_found(self):
        with self.assertRaises(NotFound):
            self.test_client.set('/schema/test/a', {'type': 'integer'})

    def test_when_getting_nonsensical_resource_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            self.test_client.get('plfo//dsf')

    def test_when_getting_non_existing_base_type_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            self.test_client.get('/hoi-daar-allemaal')

    def test_set_empty_type_data(self):
        try:
            self.test_client.set('/schema/test', {})
        except BadRequest:
            self.fail()

    def test_set_evaluation(self):
        with self.assertRaises(MethodNotAllowed):
            self.test_client.set('/evaluation/test', {})

    def test_delete_evaluation(self):
        with self.assertRaises(MethodNotAllowed):
            self.test_client.delete('/evaluation/test')
