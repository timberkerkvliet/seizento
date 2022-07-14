from unittest import TestCase

from tests.unit.unit_test_client import UnitTestClient


class TestDeleteSchema(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_Given_a_struct_schema_When_delete_field_Then_get_schema_without_field_back(self):
        self.test_client.set('schema/', {'type': 'object', 'properties': {'a': {'type': 'string'}}})

        self.test_client.delete('/schema/a')

        response = self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )

    def test_Given_an_empty_struct_schema_When_nonexisting_field_deleted_Then_get_same_schema_back(self):
        self.test_client.set('/schema', {'type': 'object'})
        self.test_client.delete('/schema/a')

        response = self.test_client.get('/schema/')
        self.assertDictEqual(
            response,
            {'type': 'object'}
        )
