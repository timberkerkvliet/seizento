from unittest import TestCase

from seizento.controllers.exceptions import BadRequest, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestArray(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_array(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'array', 'items': {'type': 'string'}}
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'array', 'items': {'type': 'string'}})

    def test_without_items(self):
        try:
            self.test_client.set('/schema/test/', {'type': 'array'})
        except BadRequest:
            self.fail()

    def test_reset_value_type(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'array', 'items': {'type': 'string'}}
        )
        self.test_client.set('/schema/test/~items', {'type': 'integer'})

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response,  {'type': 'array', 'items': {'type': 'integer'}})

    def test_cannot_remove_value_type(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'array', 'items': {'type': 'string'}}
        )
        try:
            self.test_client.delete('/schema/test/~items',)
        except Forbidden:
            self.fail()
