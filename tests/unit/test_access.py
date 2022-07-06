from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestAccess(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {
                    'read_access': ['schema/thing'],
                    'write_access': ['schema/thing']
                }
            }
        )
        await self.test_client.set(
            '/schema',
            {
                'type': 'object',
                'properties': {
                    'thing': {'type': 'string'},
                    'other-ting': {'type': 'integer'}
                }
            }
        )
        await self.test_client.login({'user_id': 'timber', 'password': 'my-password'})

    async def test_can_access(self):
        try:
            await self.test_client.get('schema/thing')
        except Unauthorized:
            self.fail()

    async def test_cannot_get_other(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.get('schema/other-thing')

    async def test_cannot_set_other(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.set('schema/other-thing', {'type': 'integer'})

    async def test_cannot_delete_other(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.delete('schema/other-thing')
