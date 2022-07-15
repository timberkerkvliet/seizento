import math
from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestFloat(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set('/schema/test/', {'type': 'number'})
        self.test_client.set(
            '/expression/test/',
            9.998
        )
        response = self.test_client.get('/expression/test/')
        self.assertTrue(math.isclose(response, 9.998))

    def test_set_wrong_literal(self):
        self.test_client.set('/schema/test/', {'type': 'number'})
        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/', 'hey')
