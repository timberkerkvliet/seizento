from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetReferenceEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_reference(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [1, '{/test/0}'])

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, [1, 1])

    def test_non_existing_key(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', ['{/test/1}'])

    def test_object_reference(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'object', 'properties': {'x': {'type': 'string'}}},
                    'b': {'type': 'object', 'properties': {'x': {'type': 'string'}}}
                }
            }
        )
        self.test_client.set(
            '/expression/test',
            {
                'a': {'x': 'copy this'},
                'b': '{/test/a}'
            }
        )

        response = self.test_client.get('/evaluation/test/')

        self.assertDictEqual(
            response,
            {
                'a': {'x': 'copy this'},
                'b': {'x': 'copy this'}
             }
        )

    def test_double_reference(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/test/', [1])

        self.test_client.set('/expression/test/1', '{/test/0}')
        self.test_client.set('/expression/test/2', '{/test/1}')

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, [1, 1, 1])
