import json
from abc import abstractmethod
from contextlib import AbstractAsyncContextManager

from seizento.domain.expression import Expression
from seizento.path import Path
from seizento.domain.types.type import Type
from seizento.serializers.path_serializer import serialize_path, serialize_component
from seizento.serializers.type_serializer import serialize_root_data, parse_type
from seizento.data_tree import DataTree


class TreeDataStoreTransaction(AbstractAsyncContextManager):
    @abstractmethod
    async def get_tree(self, path: Path) -> DataTree:
        ...

    @abstractmethod
    async def set_tree(self, path: Path, values: DataTree) -> None:
        ...

    @abstractmethod
    async def delete_tree(self, path: Path) -> None:
        ...


class Repository:
    def __init__(self, transaction: TreeDataStoreTransaction):
        self._transaction = transaction

    async def __aenter__(self):
        await self._transaction.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self._transaction.__aexit__(*args)

    def get_serialized(self, path: Path):


        base_value = json.loads(await self._transaction.get(key))

        if not sub_paths:
            return json.loads(base_value)

        return {
            **base_value,
            'subtypes': {
                serialize_component(sub_path.last_component): self.get_serialized(sub_path)
                for sub_path in sub_paths
            }
        }

    async def get_type(self, path: Path) -> Type:
        sub_paths = await self._transaction.find_sub_paths(path=path)

        result = {}
        for sub_path in sub_paths:
            self.put_in_dict(result, sub_path)

        return parse_type(self.get_serialized(path=path))

    async def set_type(self, path: Path, value: Type) -> None:
        key = f'type/{serialize_path(path)}'

        await self._key_value_store_transaction.set(
            key=key,
            value=json.dumps(serialize_root_data(value))
        )

        sub_paths = await self._key_value_store_transaction.find(key_prefix=key)

        for sub_path in sub_paths.keys():
            await self._key_value_store_transaction.delete(sub_path)

        subtypes = value.get_subtypes()
        if subtypes is None:
            return
        for component, subtype in subtypes.items():
            await self.set_type(path=path.append(component), value=subtype)

    async def get_expression(self, path: Path) -> Expression:
        pass

    async def set_expression(self, path: Path, value: Expression) -> None:
        pass
