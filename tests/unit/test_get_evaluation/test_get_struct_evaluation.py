from unittest import TestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetStructEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_not_found_before_set(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'integer'}}
            }
        )

        with self.assertRaises(NotFound):
            self.test_client.get('/evaluation/test/')

    def test_evaluation_after_change(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}}
        )
        self.test_client.set('/expression/test/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            }
        }

        self.test_client.set('/schema/test/', new_schema)

        response = self.test_client.get('/evaluation/test')

        self.assertDictEqual(response, {'a': 900})
