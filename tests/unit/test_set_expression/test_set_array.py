from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestSetArray(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_literal(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [1, 2, 3, 4])
        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, [1, 2, 3, 4])

    def test_set_empty_array(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [])

        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, [])

    def test_reset_index(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [1])
        self.test_client.set('/expression/test/0', 2)

        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, [2])

    def test_add_index(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [1])
        self.test_client.set('/expression/test/1', 2)

        response = self.test_client.get('/expression/test/')
        self.assertEqual(response, [1, 2])

    def test_set_wrong_type(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', 1)

    def test_set_wrong_value_type(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', ['a', 'b'])

    def test_set_mixing_types(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', [1, 'b'])

    def test_set_array_of_structs(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'array', 'items': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }}
        )

        self.test_client.set(
            '/expression/test/',
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

        response = self.test_client.get('/expression/test')

        self.assertEqual(
            response,
            [{'a': 5, 'b': 'hoi'}, {'a': 6, 'b': 'hey'}]
        )

    def test_set_array_of_dicts(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'array', 'items': {
                'type': 'object',
                'additionalProperties': {
                    'type': 'string'
                }
            }}
        )

        self.test_client.set(
            '/expression/test/',
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )

        response = self.test_client.get('/expression/test')

        self.assertEqual(
            response,
            [{'a': 'hey', 'b': 'hoi'}, {'x': 'tea', 'y': 'coffee'}, {}]
        )
