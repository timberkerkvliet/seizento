from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetFloatSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_float(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'number'}
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'number'})

    def test_set_optional_float(self):
        self.test_client.set('/schema/test/', {'type': ['number', 'null']})

        response = self.test_client.get('/schema/test/')
        self.assertEqual(set(response['type']), {'number', 'null'})

    def test_cannot_set_child(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'number'}
        )

        try:
            self.test_client.set(
                '/schema/test/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_cannot_set_placeholder_child(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'number'}
        )

        try:
            self.test_client.set(
                '/schema/test/~items',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()
