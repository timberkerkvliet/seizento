from unittest import IsolatedAsyncioTestCase

from tests.unit.unit_test_client import UnitTestClient


class TestDeleteSchema(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_Given_a_struct_schema_When_delete_field_Then_get_schema_without_field_back(self):
        await self.test_client.set('schema/', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )

    async def test_Given_an_empty_struct_schema_When_nonexisting_field_deleted_Then_get_same_schema_back(self):
        await self.test_client.set('/schema', {'type': 'object'})
        await self.test_client.delete('/schema/a')

        response = await self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )