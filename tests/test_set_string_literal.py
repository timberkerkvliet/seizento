from unittest import IsolatedAsyncioTestCase

from tests.test_client import UnitTestClient


class TestSetStringLiteral(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()
        await self.test_client.set(
            '/type/',
            {'name': 'STRING'}
        )

    async def test_set_and_get_expression(self):
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, 'a literal string')
