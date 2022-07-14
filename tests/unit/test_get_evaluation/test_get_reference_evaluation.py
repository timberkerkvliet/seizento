from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetReferenceEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_reference(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1, '{/0}'])

        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1])

    def test_non_existing_key(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/', ['{/1}'])

    def test_object_reference(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'object', 'properties': {'x': {'type': 'string'}}},
                    'b': {'type': 'object', 'properties': {'x': {'type': 'string'}}}
                }
            }
        )
        self.test_client.set(
            '/expression',
            {
                'a': {'x': 'copy this'},
                'b': '{/a}'
            }
        )

        response = self.test_client.get('/evaluation/')

        self.assertDictEqual(
            response,
            {
                'a': {'x': 'copy this'},
                'b': {'x': 'copy this'}
             }
        )

    def test_double_reference(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1])

        self.test_client.set('/expression/1', '{/0}')
        self.test_client.set('/expression/2', '{/1}')

        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 1, 1])
