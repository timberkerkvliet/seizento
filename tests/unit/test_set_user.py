from unittest import TestCase

from seizento.controllers.exceptions import Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestUser(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_create_new_user(self):
        self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {'read_access': [''], 'write_access': ['']}
            }
        )
        response = self.test_client.get('/user/timber/access_rights')

        self.assertDictEqual(
            {'read_access': [''], 'write_access': ['']},
            response
        )

    def test_cannot_reset_admin(self):
        with self.assertRaises(Forbidden):
            self.test_client.set(
                '/user/admin',
                {
                    'password': 'my-password',
                    'access_rights': {'read_access': [''], 'write_access': ['']}
                }
            )
