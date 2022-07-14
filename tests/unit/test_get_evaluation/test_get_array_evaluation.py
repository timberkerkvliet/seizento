from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetArrayEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1, 2, 3, 4])
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, [1, 2, 3, 4])

    def test_nested_arrays(self):
        self.test_client.set(
            '/schema/',
            {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'integer'}}}
        )
        self.test_client.set('/expression/', [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]])
        response = self.test_client.get('/evaluation/')
        self.assertEqual(response, [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]])

    def test_item_evaluation(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1, 2, 3, 4])
        response = self.test_client.get('/evaluation/1')
        self.assertEqual(response, 2)

    def test_non_existing_item(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [1, 2, 3, 4])
        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation/4')

    def test_empty_array(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})
        self.test_client.set('/expression/', [])
        response = self.test_client.get('/evaluation/')

        self.assertEqual(response, [])
