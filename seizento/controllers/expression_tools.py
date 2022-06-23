from seizento.controllers.exceptions import NotFound
from seizento.path import Path
from seizento.repository import Repository


async def find_nearest_expression(repository: Repository, path: Path):
    current_path = path
    indices = []
    while True:
        expression = await repository.get_expression(current_path)
        if expression is not None:
            break
        else:
            if path.empty:
                raise NotFound
            indices.append(path.last_component.value)
            path = path.remove_last()
            continue

    return expression, indices
