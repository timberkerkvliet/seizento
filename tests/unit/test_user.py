from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestUser(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_create_new_user(self):
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        response = await self.test_client.get('/user/timber/access_rights')

        self.assertDictEqual(
            {'read_access': [''], 'write_access': ['']},
            response
        )

    async def test_cannot_login_with_old_password_after_admin_password_reset(self):
        await self.test_client.login({'user_id': 'admin', 'password': 'admin'})
        await self.test_client.set('/user/admin/password', 'new-password')

        with self.assertRaises(Unauthorized):
            await self.test_client.login({'user_id': 'admin', 'password': 'admin'})

    async def test_can_login_with_new_password_after_admin_password_reset(self):
        await self.test_client.login({'user_id': 'admin', 'password': 'admin'})
        await self.test_client.set('/user/admin/password', 'new-password')

        try:
            await self.test_client.login({'user_id': 'admin', 'password': 'new-password'})
        except Exception:
            self.fail()

    async def test_new_user_cannot_login_with_wrong_password(self):
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

    async def test_admin_cannot_delete_itself(self):
        with self.assertRaises(Forbidden):
            await self.test_client.delete('user/admin')

    async def test_user_not_found_after_deletion(self):
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        await self.test_client.delete('/user/timber')

        with self.assertRaises(NotFound):
            await self.test_client.get('/user/timber')

    async def test_token_still_works_after_user_deletion(self):
        await self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        await self.test_client.login(data={'user_id': 'timber', 'password': 'my-password'})
        await self.test_client.delete('/user/timber')

        try:
            await self.test_client.get('/user/admin/access_rights')
        except Exception:
            self.fail()
