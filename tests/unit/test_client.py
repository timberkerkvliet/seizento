import uuid
from seizento.adapters.fake_data_tree_store import FakeDataTreeStore
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository


class UnitTestClient:
    ADMIN_TOKEN = 'admin'

    def __init__(self):
        store = FakeDataTreeStore()
        self.controller = ResourceController(
            repository_factory=lambda: Repository(store.get_transaction()),
            user_id=uuid.uuid4()
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource)
