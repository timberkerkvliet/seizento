from urllib.parse import quote, unquote

from seizento.path import PlaceHolder, StringComponent, Path, PathComponent


def parse_component(value: str) -> PathComponent:
    if value == '~':
        return PlaceHolder()

    return StringComponent(value=unquote(value))


def parse_path(value: str) -> Path:
    parts = value.split('/')

    parts = [part for part in parts if len(part) > 0]

    return Path(components=tuple([parse_component(part) for part in parts]))


def serialize_component(component: PathComponent) -> str:
    if isinstance(component, PlaceHolder):
        return '~'
    if isinstance(component, StringComponent):
        return quote(component.value)


def serialize_path(path: Path) -> str:
    return '/'.join(
        serialize_component(component) for component in path.components
    )
