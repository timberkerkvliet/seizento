from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestGetStringEvaluation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_set_and_get_literal_with_escaped_brackets(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set(
            '/expression/',
            'a literal {{ string'
        )
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal { string')

    async def test_set_and_get_literal_with_double_escaped_brackets(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set(
            '/expression/',
            '{{a}}'
        )
        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, '{a}')

    async def test_set_and_evaluate_literal(self):
        await self.test_client.set('/schema/', {'type': 'string'})
        await self.test_client.set('/expression/', 'a literal string')

        response = await self.test_client.get('/evaluation/')
        self.assertEqual(response, 'a literal string')

    async def test_missing_value(self):
        await self.test_client.set('/schema/', {'type': 'string'})

        with self.assertRaises(NotFound):
            await self.test_client.get('/evaluation')
