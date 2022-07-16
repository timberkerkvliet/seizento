from unittest import TestCase

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestSetReference(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_reference_with_wrong_type(self):
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
        self.test_client.set('/expression/test', {'a': 5})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test/b', '{/a}')

    def test_self_reference(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/test', ['{/0}'])

    def test_self_reference_did_not_change_anything(self):
        self.test_client.set('/schema/test/', {'type': 'array', 'items': {'type': 'integer'}})

        self.test_client.set('/expression/test', [1])

        try:
            self.test_client.set('/expression/test', ['{/test/0}'])
        except Forbidden:
            pass

        response = self.test_client.get('/expression/test')

        self.assertEqual(response, [1])

    def test_self_reference_did_not_set_anything(self):
        self.test_client.set('/schema/test/', {'type': 'string'})

        try:
            self.test_client.set('/expression/test', '{/test/}')
        except Forbidden:
            pass

        with self.assertRaises(NotFound):
            self.test_client.get('/expression/test')
