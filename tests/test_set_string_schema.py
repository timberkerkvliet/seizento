from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestSetStringSchema(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_with_only_name(self):
        await self.test_client.set(
            '/type/',
            {'name': 'STRING'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(response, {'name': 'STRING', 'default_value': None, 'optional': False})

    async def test_optional(self):
        await self.test_client.set(
            '/type/',
            {'name': 'STRING', 'optional': True}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(response, {'name': 'STRING', 'default_value': None, 'optional': True})

    async def test_default_value(self):
        await self.test_client.set(
            '/type/',
            {'name': 'STRING', 'default_value': 'some-default'}
        )

        response = await self.test_client.get('/type/')
        self.assertDictEqual(response, {'name': 'STRING', 'default_value': 'some-default', 'optional': False})
