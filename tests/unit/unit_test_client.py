import jwt

from seizento.adapters.in_memory_data_tree_store import InMemoryDataTreeStore
from seizento.controllers.resource_controller import ResourceController
from seizento.path import EMPTY_PATH
from seizento.serializers.user_serializer import serialize_access_rights
from seizento.user import AccessRights


class UnitTestClient:
    def __init__(self):
        store = InMemoryDataTreeStore()
        self.controller = ResourceController(
            transaction_factory=lambda: store.get_transaction(),
            token_secret='test-secret'
        )
        self.admin_token = jwt.encode(
            payload=serialize_access_rights(
                AccessRights(read_access={EMPTY_PATH}, write_access={EMPTY_PATH})
            ),
            key='test-secret'
        )

    async def get(self, resource: str):
        return await self.controller.get(resource=resource, token=self.admin_token)

    async def set(self, resource: str, data):
        await self.controller.set(resource=resource, data=data, token=self.admin_token)

    async def delete(self, resource: str) -> None:
        await self.controller.delete(resource=resource, token=self.admin_token)
