from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import NotFound, Unauthorized, Forbidden
from tests.unit.unit_test_client import UnitTestClient


class TestUser(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

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
