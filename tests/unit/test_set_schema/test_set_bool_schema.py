from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetBoolSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_bool(self):
        self.test_client.set('/schema/', {'type': 'boolean'})

        response = self.test_client.get('/schema/')
        self.assertDictEqual(response, {'type': 'boolean'})

    def test_set_optional_bool(self):
        self.test_client.set('/schema/', {'type': ['boolean', 'null']})

        response = self.test_client.get('/schema/')
        self.assertEqual(set(response['type']), {'boolean', 'null'})

    def test_can_set_child(self):
        self.test_client.set(
            '/schema/',
            {'type': 'boolean'}
        )

        try:
            self.test_client.set(
                '/schema/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_can_set_placeholder_child(self):
        self.test_client.set(
            '/schema/',
            {'type': 'boolean'}
        )

        try:
            self.test_client.set(
                '/schema/~items',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()