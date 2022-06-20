from urllib.parse import quote, unquote

from seizento.domain.path import PlaceHolder, PathValue, Path, PathComponent


def parse_component(value: str) -> PathComponent:
    if value == '~':
        return PlaceHolder()

    return PathValue(value=unquote(value))


def parse_path(value: str) -> Path:
    parts = value.split('/')

    return Path(components=[parse_component(part) for part in parts])


def serialize_component(component: PathComponent) -> str:
    if isinstance(component, PlaceHolder):
        return '~'
    if isinstance(component, PathValue):
        return quote(component.value)


def serialize_path(path: Path) -> str:
    return '/'.join(
        serialize_component(component) for component in path.components
    )
