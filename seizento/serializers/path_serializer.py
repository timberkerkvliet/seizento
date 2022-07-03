from urllib.parse import quote, unquote

from seizento.path import PlaceHolder, LiteralComponent, Path, PathComponent


def parse_component(value: str) -> PathComponent:
    if value == '~':
        return PlaceHolder()

    return LiteralComponent(value=unquote(value))


def parse_path(value: str) -> Path:
    parts = value.split('/')

    if len(parts) > 0 and parts[0] == '':
        parts = parts[1:]

    if len(parts) > 0 and parts[-1] == '':
        parts = parts[:-1]

    return Path(components=tuple([parse_component(part) for part in parts]))


def serialize_component(component: PathComponent) -> str:
    if isinstance(component, PlaceHolder):
        return '~'
    if isinstance(component, LiteralComponent):
        return quote(component.value)


def serialize_path(path: Path) -> str:
    return '/'.join(
        serialize_component(component) for component in path.components
    )
