from __future__ import annotations

from dataclasses import dataclass
from typing import Set, TYPE_CHECKING, Union

from seizento.data_tree import DataTree
from seizento.expression.expression import Expression, ArgumentSpace
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, MatchComponent, EMPTY_PATH
from seizento.schema.schema import Schema

if TYPE_CHECKING:
    from seizento.expression.path_service import PathService


@dataclass(frozen=True)
class PathReference(Expression):
    reference: list[Union[LiteralComponent, Identifier]]

    @property
    def path(self) -> Path:
        return Path(
            components=tuple(
                x if isinstance(x, LiteralComponent) else MatchComponent()
                for x in self.reference
            )
        )

    def get_schema(self, schemas: dict[Path, Schema]) -> Schema:
        return schemas[self.path]

    def _get_argument_space(self, value, parts) -> ArgumentSpace:
        if len(parts) == 0:
            return ArgumentSpace(values={})

        part = parts[0]

        if isinstance(part, LiteralComponent):
            index = part.value if isinstance(value, dict) else int(part.value)
            return self._get_argument_space(value[index], parts[1:])

        if isinstance(part, Identifier) and isinstance(value, dict):
            result = ArgumentSpace(values={part: set(value.keys())})
            for val in value.values():
                result = result.intersect(self._get_argument_space(val, parts[1:]))

            return result

        if isinstance(part, Identifier) and isinstance(value, list):
            result = ArgumentSpace(values={part: set(str(x) for x in range(len(value)))})
            for val in value:
                result = result.intersect(self._get_argument_space(val, parts[1:]))

            return result

        raise TypeError

    async def get_argument_space(
        self,
        path_service: PathService
    ) -> ArgumentSpace:
        parts = self.reference
        path = EMPTY_PATH
        while len(parts) > 0 and isinstance(parts[0], LiteralComponent):
            path = path.append(parts[0])
            parts = parts[1:]

        root_value = await path_service.evaluate(path=path)

        return self._get_argument_space(value=root_value, parts=parts)

    async def evaluate(
        self,
        path_service: PathService,
        arguments: dict[Identifier, str]
    ):
        path = Path(
            components=tuple(
                x if isinstance(x, LiteralComponent) else LiteralComponent(str(arguments[x])) for x in self.reference
            )
        )

        return await path_service.evaluate(path=path)

    def get_path_references(self) -> Set[Path]:
        return {self.path}

    def supports_child_at(self, component: PathComponent) -> bool:
        return False

    def to_tree(self) -> DataTree:
        return DataTree(root_data=self)
