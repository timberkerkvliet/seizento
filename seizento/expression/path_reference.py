from __future__ import annotations

from dataclasses import dataclass
from typing import Set, TYPE_CHECKING, Union

from seizento.expression.expression import Expression, ArgumentSpace
from seizento.identifier import Identifier
from seizento.path import Path, PathComponent, LiteralComponent, EMPTY_PATH, PlaceHolder
from seizento.schema.schema import Schema


from seizento.expression.path_evaluation import evaluate_expression_at_path


@dataclass
class PathReference(Expression):
    reference: list[Union[LiteralComponent, Identifier]]

    def get_schema(self, root_schema: Schema) -> Schema:
        result = root_schema

        for x in self.reference:
            component = x if isinstance(x, LiteralComponent) else PlaceHolder()
            result = result.get_child(component)

        return result

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

    def get_argument_space(
        self,
        root_expression: Expression,
    ) -> ArgumentSpace:
        parts = self.reference
        path = EMPTY_PATH
        while len(parts) > 0 and isinstance(parts[0], LiteralComponent):
            path = path.append(parts[0])
            parts = parts[1:]

        root_value = evaluate_expression_at_path(path=path, root_expression=root_expression)

        return self._get_argument_space(value=root_value, parts=parts)

    def evaluate(
        self,
        root_expression: Expression,
        arguments: dict[Identifier, str]
    ):
        path = Path(
            components=tuple(
                x if isinstance(x, LiteralComponent) else LiteralComponent(str(arguments[x])) for x in self.reference
            )
        )

        return evaluate_expression_at_path(path=path, root_expression=root_expression)

    def get_child(self, component: PathComponent) -> None:
        raise KeyError

    def set_child(self, component: PathComponent, expression: Expression) -> None:
        raise ValueError

    def delete_child(self, component: PathComponent) -> None:
        return

