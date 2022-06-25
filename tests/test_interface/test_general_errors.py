from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, BadRequest, Forbidden
from tests.test_interface.test_client import UnitTestClient


class TestGeneralErrors(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_when_setting_schema_with_no_paren_then_raise_not_found(self):
        with self.assertRaises(NotFound):
            await self.test_client.set('/schema/a', {'type': 'integer'})

    async def test_when_setting_expression_with_no_paren_then_raise_not_found(self):
        await self.test_client.set('/schema/', {'type': 'object', 'properties': {'a': {'type': 'integer'}}})
        with self.assertRaises(NotFound):
            await self.test_client.set('/expression/a', 99)

    async def test_given_a_non_literal_parent_expression_when_setting_expression_then_raise_forbidden(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'array', 'items': {'type': 'integer'}},
                    'b': {'type': 'array', 'items': {'type': 'integer'}}
                }
            }
        )
        await self.test_client.set(
            '/expression',
            {
                'a': [1, 2, 3, 4],
                'b': '{/a}'
            }
        )

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/b/0', 5)

    async def test_when_getting_nonsensical_resource_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            await self.test_client.get('plfo//dsf')

    async def test_when_getting_non_existing_base_type_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            await self.test_client.get('/hoi-daar-allemaal')

    async def test_set_empty_type_data(self):
        with self.assertRaises(BadRequest):
            await self.test_client.set('/schema', {})
