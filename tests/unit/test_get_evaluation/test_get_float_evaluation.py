import math
from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetFloatEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set(self):
        self.test_client.set('/schema/', {'type': 'number'})
        self.test_client.set('/expression/', -4.56)

        response = self.test_client.get('/evaluation/')
        self.assertTrue(math.isclose(response, -4.56))

    def test_not_set(self):
        self.test_client.set('/schema/', {'type': 'number'})

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation')
