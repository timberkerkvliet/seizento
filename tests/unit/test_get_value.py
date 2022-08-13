from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Unauthorized
from tests.unit.unit_test_client import UnitTestClient


class TestGetDictionaryEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_set_and_get_literal(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/value/test/', {'a': 44, 'p': 99})
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'a': 44, 'p': 99})

    def test_nested_dicts(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'additionalProperties': {
                    'type': 'object',
                    'additionalProperties': {'type': 'integer'}
                }
            }
        )
        self.test_client.set('/value/test/', {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {'a': {'hey': 5}, 'p': {'a': 1, 'b': 2}})

    def test_item_evaluation(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/value/test/', {'a': 44, 'p': 99})
        response = self.test_client.get('/value/test/p')
        self.assertEqual(response, 99)

    def test_non_existing_item(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/value/test/', {'a': 44, 'p': 99})

        with self.assertRaises(NotFound):
            self.test_client.get('/value/test/pq')

    def test_empty_object(self):
        self.test_client.set('/schema/test/', {'type': 'object', 'additionalProperties': {'type': 'integer'}})
        self.test_client.set('/value/test/', {})
        response = self.test_client.get('/value/test/')
        self.assertEqual(response, {})

    def test_not_found_before_set(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {'a': {'type': 'integer'}}
            }
        )

        with self.assertRaises(NotFound):
            self.test_client.get('/value/test/')

    def test_evaluation_after_change(self):
        self.test_client.set(
            '/schema/test/',
            {'type': 'object', 'properties': {'a': {'type': 'integer'}}}
        )
        self.test_client.set('/value/test/',  {'a': 900})

        new_schema = {
            'type': 'object',
            'properties': {
                'a': {'type': 'integer'},
                'b': {'type': 'integer'}
            }
        }

        self.test_client.set('/schema/test/', new_schema)

        response = self.test_client.get('/value/test')

        self.assertDictEqual(response, {'a': 900})

    def test_can_get_authorized_value(self):
        self.test_client.set(
            '/user/timber',
            {
                'access_rights': {
                    'read_access': ['value/my-thing'],
                    'write_access': ['schema/my-thing']
                },
                'password': 'a'
             }
        )

        self.test_client.set('schema/my-thing', {'type': 'string'})
        self.test_client.set('value/my-thing', 'a string')
        self.test_client.login({'user_id': 'timber', 'password': 'a'})

        try:
            self.test_client.get('value/my-thing')
        except Unauthorized:
            self.fail()
