from typing import Dict, Type, Any
from uuid import UUID

from seizento.domain.path import Path
from seizento.repository import Repository
from seizento.serializers.type_serializer import serialize_type



class Controller:
    def __init__(
        self,
        repository: Repository,
        user_id: UUID,
        token: str
    ):
        self._repository = repository
        self._user_id = user_id
        self._token = token

    async def get_resource(self, resource: str) -> Dict:
        parts = resource.split('/')

        target_type = await self._repository.get_type(path=path)

        return serialize_type(target_type)

    async def set_resource(self, resource: str, data: Any) -> None:
        await self._repository.set_type(path=path, value=new_value)

    async def delete_resource(self, resource: str) -> None:
        await self._repository.set_type(path=path)

