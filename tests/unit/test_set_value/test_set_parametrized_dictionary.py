from unittest import TestCase

from tests.unit.unit_test_client import UnitTestClient


class TestSetParametrizedDictionary(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()
