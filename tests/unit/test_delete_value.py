from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestDeleteValue(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_delete(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set(
            '/value/test/',
            {'a': 1001, 'b': 'nachten'}
        )
        self.test_client.delete('value/test/a')
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'b': 'nachten'})
