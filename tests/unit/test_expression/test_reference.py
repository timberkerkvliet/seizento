from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.test_client import UnitTestClient


class TestReference(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_reference_with_wrong_type(self):
        await self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        await self.test_client.set('/expression', {'a': 5})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/b', '{/a}')

    async def test_cycle_of_three(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        await self.test_client.set('/expression/', ['{/1}', '{/2}'])

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression/2', '{/0}')

    async def test_self_reference(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            await self.test_client.set('/expression', ['{/0}'])

    async def test_self_reference_did_not_change_anything(self):
        await self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        await self.test_client.set('/expression', [1])

        try:
            await self.test_client.set('/expression', ['{/0}'])
        except Forbidden:
            pass

        response = await self.test_client.get('/expression')

        self.assertEqual(response, [1])
