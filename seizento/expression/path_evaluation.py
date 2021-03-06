from seizento.controllers.exceptions import NotFound
from seizento.expression.expression import Expression
from seizento.path import Path, EMPTY_PATH


def evaluate_expression_at_path(path: Path, root_expression: Expression):
    current_path = EMPTY_PATH
    expression = root_expression
    for component in path:
        try:
            expression = expression.get_child(component)
        except KeyError:
            break

        current_path = current_path.append(component)

    indices = [
        int(component.value) if component.value.isdigit() else component.value
        for component in path.components[len(current_path):]
    ]

    evaluation = expression.evaluate(root_expression=root_expression, arguments={})

    for index in indices:
        try:
            evaluation = evaluation[index]
        except (KeyError, IndexError):
            raise NotFound

    return evaluation
