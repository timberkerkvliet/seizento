from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestStruct(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set(
            '/expression/',
            {'a': 1001, 'b': 'nachten'}
        )
        response = self.test_client.get('/expression/')
        self.assertEqual(response, {'a': 1001, 'b': 'nachten'})

    async def test_set_partially(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set(
            '/expression/',
            {'a': 1001}
        )
        response = self.test_client.get('/expression/')
        self.assertEqual(response, {'a': 1001})

    async def test_empty(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set('/expression/', {})
        response = self.test_client.get('/expression/')
        self.assertEqual(response, {})

    async def test_get_field_expression(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'}
                }
            }
        )
        self.test_client.set('/expression/', {'a': 9})

        response = self.test_client.get('expression/a')

        self.assertEqual(response, 9)

    async def test_nested_struct(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'object',
                        'properties': {
                            'b': {'type': 'integer'}
                        }
                    }
                }
            }
        )
        self.test_client.set('/expression', {'a': {'b': 99}})

        response = self.test_client.get('/expression/a/b')

        self.assertEqual(response, 99)

    async def test_given_a_non_literal_parent_expression_when_setting_expression_then_raise_forbidden(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'array', 'items': {'type': 'integer'}},
                    'b': {'type': 'array', 'items': {'type': 'integer'}}
                }
            }
        )
        self.test_client.set(
            '/expression',
            {
                'a': [1, 2, 3, 4],
                'b': '{/a}'
            }
        )

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/b/0', 5)

    async def test_when_setting_expression_with_no_paren_then_raise_not_found(self):
        self.test_client.set('/schema/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        with self.assertRaises(NotFound):
            self.test_client.set('/expression/a', 99)

    async def test_add_field_after_expression_has_been_set(self):
        self.test_client.set('/schema/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        self.test_client.set('/expression', {'a': 19})
        self.test_client.set('/schema/b', {'type': 'string'})
        self.test_client.set('/expression/b', 'hallo')

        response = self.test_client.get('expression')

        self.assertDictEqual({'a': 19, 'b': 'hallo'}, response)
