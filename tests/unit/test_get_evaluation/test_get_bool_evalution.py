from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetBoolEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_true(self):
        self.test_client.set('/schema/test/', {'type': 'boolean'})
        self.test_client.set('/expression/test/', True)

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, True)

    def test_set_false(self):
        self.test_client.set('/schema/test/', {'type': 'boolean'})
        self.test_client.set('/expression/test/', False)

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, False)

    def test_not_set(self):
        self.test_client.set('/schema/test/', {'type': 'boolean'})

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation/test')
