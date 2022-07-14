from unittest import TestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestGetUser(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_cannot_access_other_user(self):
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
        self.test_client.login({'user_id': 'timber', 'password': 'my-password'})
        with self.assertRaises(Unauthorized):
            self.test_client.get('user/admin/access_rights')

    def test_cannot_access_password(self):
        with self.assertRaises(NotFound):
            self.test_client.get('user/admin/password')

    def test_cannot_access_complete_user(self):
        with self.assertRaises(NotFound):
            self.test_client.get('user/admin')
