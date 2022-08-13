from unittest import TestCase

from seizento.controllers.exceptions import Unauthorized
from tests.unit.unit_test_client import UnitTestClient


class TestAccess(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()
        self.test_client.set(
            '/user/timber',
            {
                'password': 'my-password',
                'access_rights': {
                    'read_access': ['schema/test/thing'],
                    'write_access': ['schema/test/thing']
                }
            }
        )
        self.test_client.set(
            '/schema/test',
            {
                'type': 'object',
                'properties': {
                    'thing': {'type': 'string'},
                    'other-thing': {'type': 'integer'}
                }
            }
        )
        self.test_client.login({'user_id': 'timber', 'password': 'my-password'})

    def test_set_schema__has_write_access__no_authorization_error(self):
        try:
            self.test_client.set('schema/test/thing', {'type': 'integer'})
        except Unauthorized:
            self.fail()

    def test_delete_schema__has_write_access__no_authorization_error(self):
        try:
            self.test_client.delete('schema/test/thing')
        except Unauthorized:
            self.fail()

    def test_set_schema__no_write_access__authorization_error(self):
        with self.assertRaises(Unauthorized):
            self.test_client.set('schema/test/other-thing', {'type': 'integer'})

    def test_delete_schema__no_write_access__authorization_error(self):
        with self.assertRaises(Unauthorized):
            self.test_client.delete('schema/test/other-thing')
