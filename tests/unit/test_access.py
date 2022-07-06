from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Unauthorized
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
                    'other-thing': {'type': 'integer'}
                }
            }
        )
        await self.test_client.login({'user_id': 'timber', 'password': 'my-password'})

    async def test_get_schema__has_read_access__no_authorization_error(self):
        try:
            await self.test_client.get('schema/thing')
        except Unauthorized:
            self.fail()

    async def test_set_schema__has_write_access__no_authorization_error(self):
        try:
            await self.test_client.set('schema/thing', {'type': 'integer'})
        except Unauthorized:
            self.fail()

    async def test_delete_schema__has_write_access__no_authorization_error(self):
        try:
            await self.test_client.delete('schema/thing')
        except Unauthorized:
            self.fail()

    async def test_get_schema__no_read_access__authorization_error(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.get('schema/other-thing')

    async def test_set_schema__no_write_access__authorization_error(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.set('schema/other-thing', {'type': 'integer'})

    async def test_delete_schema__no_write_access__authorization_error(self):
        with self.assertRaises(Unauthorized):
            await self.test_client.delete('schema/other-thing')
