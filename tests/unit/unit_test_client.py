from seizento.adapters.in_memory_data_tree_store import InMemoryDataTreeStore
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController
from seizento.schema.constraint import EverythingAllowed
from seizento.schema.schema import Schema

from seizento.user import ADMIN_USER


class UnitTestClient:
    def __init__(self):
        store = InMemoryDataTreeStore(admin_user=ADMIN_USER)
        root_schema = Schema(properties={'schema': EverythingAllowed()})

        self.resource_controller = ResourceController(
            transaction_factory=lambda: store.get_transaction(),
            app_secret='test-secret',
            root_schema=root_schema
        )
        self.login_controller = LoginController(
            transaction_factory=lambda: store.get_transaction(),
            app_secret='test-secret',
            root_schema=root_schema
        )
        self.token = None

    async def login(self, data=None):
        data = data or {
            'user_id': 'admin',
            'password': 'admin'
        }
        self.token = await self.login_controller.login(data)

    async def get(self, resource: str):
        if self.token is None:
            await self.login()
        return await self.resource_controller.get(resource=resource, token=self.token)

    async def set(self, resource: str, data):
        if self.token is None:
            await self.login()
        await self.resource_controller.set(resource=resource, data=data, token=self.token)

    async def delete(self, resource: str) -> None:
        if self.token is None:
            await self.login()
        await self.resource_controller.delete(resource=resource, token=self.token)
