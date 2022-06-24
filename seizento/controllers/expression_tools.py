from dataclasses import dataclass
from typing import Optional

from seizento.domain.expression import Expression
from seizento.path import Path
from seizento.repository import Repository


@dataclass(frozen=True)
class NearestExpressionResult:
    expression: Expression
    path: Path


async def find_nearest_expression(repository: Repository, path: Path) -> Optional[NearestExpressionResult]:
    current_path = path
    while True:
        expression = await repository.get_expression(current_path)
        if expression is not None:
            return NearestExpressionResult(
                expression=expression,
                path=current_path
            )

        if path.empty:
            return None

        path = path.remove_last()
        continue
