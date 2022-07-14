from dataclasses import dataclass
from typing import Set

from seizento.controllers.exceptions import NotFound
from seizento.expression.expression import Expression
from seizento.path import Path, EMPTY_PATH


@dataclass
class NearestExpressionResult:
    expression: Expression
    path: Path


def find_nearest_expression(path: Path, root_expression: Expression) -> NearestExpressionResult:
    current_path = EMPTY_PATH
    expression = root_expression
    for component in path:
        try:
            expression = expression.get_child(component)
        except KeyError:
            break

        current_path = current_path.append(component)

    return NearestExpressionResult(
        expression=expression,
        path=current_path
    )


def evaluate_expression_at_path(path: Path, root_expression: Expression):
    nearest_expression = find_nearest_expression(path=path, root_expression=root_expression)

    indices = [
        int(component.value) if component.value.isdigit() else component.value
        for component in path.components[len(nearest_expression.path):]
    ]
    expression = nearest_expression.expression

    evaluation = expression.evaluate(root_expression=root_expression, arguments={})

    for index in indices:
        try:
            evaluation = evaluation[index]
        except (KeyError, IndexError):
            raise NotFound

    return evaluation
