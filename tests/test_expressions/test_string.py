from unittest import IsolatedAsyncioTestCase, skip

from seizento.controllers.exceptions import Forbidden
from tests.test_client import UnitTestClient


class TestString(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal(self):
        await self.test_client.set('/type/', {'name': 'STRING'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/expression/')
        self.assertEqual(response, 'a literal string')

    async def test_set_and_evaluate_literal(self):
        await self.test_client.set('/type/', {'name': 'STRING'})
        await self.test_client.set(
            '/expression/',
            'a literal string'
        )
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    async def test_set_wrong_literal(self):
        await self.test_client.set('/type/', {'name': 'STRING'})
        with self.assertRaises(Forbidden):
            await self.test_client.set(
                '/expression/',
                9000
            )

    @skip
    async def test_set_and_evaluate_expression(self):
        await self.test_client.set(
            '/type/',
            {
                'name': 'STRUCT',
                'children': {
                    'my-string': {'name': 'STRING'},
                    'other-string': {'name': 'STRING'}
                }
            }
        )
        await self.test_client.set(
            '/expression/my-string',
            '{other-string}'
        )
