from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, BadRequest, MethodNotAllowed
from tests.unit.unit_test_client import UnitTestClient


class TestGeneralErrors(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_when_setting_schema_with_no_paren_then_raise_not_found(self):
        with self.assertRaises(NotFound):
            await self.test_client.set('/schema/a', {'type': 'integer'})

    async def test_when_getting_nonsensical_resource_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            await self.test_client.get('plfo//dsf')

    async def test_when_getting_non_existing_base_type_then_raise_bad_request(self):
        with self.assertRaises(BadRequest):
            await self.test_client.get('/hoi-daar-allemaal')

    async def test_set_empty_type_data(self):
        try:
            await self.test_client.set('/schema', {})
        except BadRequest:
            self.fail()

    async def test_set_evaluation(self):
        with self.assertRaises(MethodNotAllowed):
            await self.test_client.set('/evaluation', {})

    async def test_delete_evaluation(self):
        with self.assertRaises(MethodNotAllowed):
            await self.test_client.delete('/evaluation')
