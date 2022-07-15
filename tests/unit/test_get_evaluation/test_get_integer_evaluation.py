from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetIntegerEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_positive(self):
        self.test_client.set('/schema/test/', {'type': 'integer'})
        self.test_client.set('/expression/test/', 10)

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, 10)

    def test_set_zero(self):
        self.test_client.set('/schema/test/', {'type': 'integer'})
        self.test_client.set('/expression/test/', 0)

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, 0)

    def test_set_negative(self):
        self.test_client.set('/schema/test/', {'type': 'integer'})
        self.test_client.set('/expression/test/', -100)

        response = self.test_client.get('/evaluation/test/')
        self.assertEqual(response, -100)

    def test_not_set(self):
        self.test_client.set('/schema/test/', {'type': 'integer'})

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation/test')
