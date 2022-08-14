from unittest import TestCase

from seizento.controllers.exceptions import Unauthorized
from tests.unit.unit_test_client import UnitTestClient


class TestUser(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_cannot_login_with_old_password_after_admin_password_reset(self):
        self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'my-password'})
        self.test_client.set('/user/timber/password', 'new-password')

        with self.assertRaises(Unauthorized):
            self.test_client.login({'user_id': 'timber', 'password': 'my-password'})

    def test_can_login_with_new_password_after_admin_password_reset(self):
        self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'my-password'})
        self.test_client.set('/user/timber/password', 'new-password')

        try:
            self.test_client.login({'user_id': 'timber', 'password': 'new-password'})
        except Exception:
            self.fail()

    def test_new_user_cannot_login_with_wrong_password(self):
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
