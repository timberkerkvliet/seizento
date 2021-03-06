from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetIntegerSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_integer(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'integer'}
        )

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(response, {'type': 'integer'})

    def test_set_optional_integer(self):
        self.test_client.set('/schema/test/', {'type': ['integer', 'null']})

        response = self.test_client.get('/schema/test/')
        self.assertEqual(set(response['type']), {'integer', 'null'})

    def test_cannot_set_child(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'integer'}
        )

        try:
            self.test_client.set(
                '/schema/test/a',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_can_set_placeholder_child(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'integer'}
        )

        try:
            self.test_client.set(
                '/schema/test/~items',
                {'type': 'integer'}
            )
        except Forbidden:
            self.fail()

    def test_can_set_integer_if_string_is_set(self):
        self.test_client.set('/schema/test/', {'type': 'string'})

        try:
            self.test_client.set('/schema/test/', {'type': 'integer'})
        except Forbidden:
            self.fail()

    def test_change_to_integer_after_string_expression_has_set(self):
        self.test_client.set('/schema/test/', {'type': 'string'})
        self.test_client.set('/expression/test/', 'hey')

        with self.assertRaises(Forbidden):
            self.test_client.set('/schema/test/', {'type': 'integer'})

    def test_set_struct_field_to_integer(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'number'}, 'b': {'type': 'string'}}
            }
        )

        self.test_client.set('/schema/test/a', {'type': 'integer'})

        response = self.test_client.get('/schema/test/')
        self.assertDictEqual(
            response,
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }

            }
        )
