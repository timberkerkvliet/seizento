from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized
from tests.unit.unit_test_client import UnitTestClient


class TestUserCreation(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_create_new_user(self):
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {
                    'read_access': [''],
                    'write_access': ['']
                }
            }
        )
        response = await self.test_client.get('/user/timber/access_rights')

        self.assertDictEqual(
            {
                'read_access': [''],
                'write_access': ['']
            },
            response
        )

    async def test_reset_own_password(self):
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
        await self.test_client.set('/user/timber/password', 'new-password')
        await self.test_client.login({'user_id': 'timber', 'password': 'new-password'})

        response = await self.test_client.get('user/timber/access_rights')

        self.assertDictEqual(
            {
                'read_access': ['user/timber'],
                'write_access': ['user/timber']
            },
            response
        )

    async def test_wrong_password(self):
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

        with self.assertRaises(Unauthorized):
            await self.test_client.login({'user_id': 'timber', 'password': 'not-my-password'})

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
