from __future__ import annotations

from dataclasses import dataclass

from jsonschema.exceptions import ValidationError, SchemaError

from seizento.path import PathComponent, LiteralComponent, PropertyPlaceHolder, IndexPlaceHolder, Path

from jsonschema import validate

from seizento.value_type import JsonValue


class InvalidSchema(Exception):
    pass


@dataclass
class Schema:
    schema: JsonValue

    def __post_init__(self):
        try:
            validate(instance=None, schema=self.schema)
        except ValidationError:
            pass
        except SchemaError as e:
            raise InvalidSchema from e

    def validate_value(self, value) -> None:
        validate(instance=value, schema=self.schema)

    def navigate_to(self, path: Path) -> Schema:
        result = self
        for component in path:
            result = result.get_child(component)

        return result

    def get_child(self, component: PathComponent) -> Schema:
        if isinstance(component, LiteralComponent) \
            and 'properties' in self.schema \
                and component.value in self.schema['properties']:
            return Schema(self.schema['properties'][component.value])
        if isinstance(component, LiteralComponent) \
                and isinstance(component.value, int)\
                and (len(self.schema.get('type', {})) == 0 or 'array' in self.schema.get('type')):
            return Schema(self.schema.get('items', {}))
        if component == IndexPlaceHolder():
            return Schema(self.schema.get('items', {}))
        if component == PropertyPlaceHolder():
            return Schema(self.schema.get('additionalProperties', {}))

        if 'additionalProperties' in self.schema and self.schema['additionalProperties'] is False:
            raise KeyError

        return Schema({})

    def set_child(self, component: PathComponent, schema: Schema) -> None:
        if isinstance(component, LiteralComponent):
            if 'properties' not in self.schema:
                self.schema['properties'] = {}
            self.schema['properties'][component.value] = schema.schema
        if component == PropertyPlaceHolder():
            self.schema['additionalProperties'] = schema.schema
        if component == IndexPlaceHolder():
            self.schema['items'] = schema.schema

    def delete_child(self, component: PathComponent) -> None:
        if isinstance(component, LiteralComponent) and 'properties' in self.schema:
            self.schema['properties'].pop(component.value, None)
