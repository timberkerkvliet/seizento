from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetUser(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_cannot_access_other_user(self):
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {
                    'read_access': ['user/timber'],
                    'write_access': ['user/timber']
                }
            }
        )
        await self.test_client.login({'user_id': 'timber', 'password': 'my-password'})
        with self.assertRaises(Unauthorized):
            await self.test_client.get('user/admin/access_rights')

    async def test_cannot_access_password(self):
        with self.assertRaises(NotFound):
            await self.test_client.get('user/admin/password')

    async def test_cannot_access_complete_user(self):
        with self.assertRaises(NotFound):
            await self.test_client.get('user/admin')
