from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestDictionary(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_dict(self):
        self.test_client.set(
            '/schema/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'object', 'additionalProperties': {'type': 'string'}})

    def test_reset_value_type(self):
        self.test_client.set(
            '/schema/',
            {'type': 'object', 'additionalProperties': {'type': 'string'}}
        )
        self.test_client.set(
            '/schema/~properties',
            {'type': 'integer'}
        )

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response,  {'type': 'object', 'additionalProperties': {'type': 'integer'}})

    def test_set_dict_from_struct(self):
        self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'properties': {'a': {'type': 'string'}},
                'additionalProperties': False
            }
        )
        self.test_client.set('/expression', {'a': 'a'})

        try:
            self.test_client.set('/schema', {'type': 'object', 'additionalProperties': {'type': 'string'}})
        except Forbidden:
            self.fail()
