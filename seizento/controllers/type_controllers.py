from typing import Dict

from seizento.domain.path import Path
from seizento.domain.type import Type, Struct, Dictionary, Array, Function, String, Float
from seizento.repositories import TypeRepository
from seizento.serializers.type_serializer import serialize_type


async def get_type(root: str, path: Path, type_repository: TypeRepository) -> Dict:
    root_type = await type_repository.get(root=root)
    target_type = root_type.get_subtype(path=path)

    return serialize_type(target_type)


async def set_type(root: str, path: Path, data: Dict, type_repository: TypeRepository) -> None:
    root_type = await type_repository.get(root=root)

    type = root_type.get_subtype(path=path)


    await type_repository.set(root=root, type=type)

