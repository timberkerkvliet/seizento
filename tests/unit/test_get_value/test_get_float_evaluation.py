import math
from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetFloatEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set(self):
        self.test_client.set('/schema/test/', {'type': 'number'})
        self.test_client.set('/value/test/', -4.56)

        response = self.test_client.get('/value/test/')
        self.assertTrue(math.isclose(response, -4.56))

    def test_not_set(self):
        self.test_client.set('/schema/test/', {'type': 'number'})

        with self.assertRaises(NotFound):
            self.test_client.get('/value/test')
