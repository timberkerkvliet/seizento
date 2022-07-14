from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestUser(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_cannot_login_with_old_password_after_admin_password_reset(self):
        self.test_client.login({'user_id': 'admin', 'password': 'admin'})
        self.test_client.set('/user/admin/password', 'new-password')

        with self.assertRaises(Unauthorized):
            self.test_client.login({'user_id': 'admin', 'password': 'admin'})

    async def test_can_login_with_new_password_after_admin_password_reset(self):
        self.test_client.login({'user_id': 'admin', 'password': 'admin'})
        self.test_client.set('/user/admin/password', 'new-password')

        try:
            self.test_client.login({'user_id': 'admin', 'password': 'new-password'})
        except Exception:
            self.fail()

    async def test_new_user_cannot_login_with_wrong_password(self):
        self.test_client.set(
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
            self.test_client.login({'user_id': 'timber', 'password': 'not-my-password'})
