from dataclasses import dataclass
from typing import Dict

from seizento.expression.expression import Expression
from seizento.expression.struct_literal import StructLiteral
from seizento.identifier import Identifier
from seizento.schema.schema import Schema
from seizento.schema.types import DataType
from seizento.serializers.constraint_serializer import serialize_constraint
from seizento.serializers.expression_serializer import serialize_expression
from seizento.serializers.user_serializer import serialize_user
from seizento.user import User, ADMIN_USER


@dataclass
class ApplicationData:
    schema: Schema
    expression: Expression
    users: Dict[Identifier, User]


def create_default() -> ApplicationData:
    return ApplicationData(
        schema=Schema(types={DataType.OBJECT}),
        expression=StructLiteral(values={}),
        users={ADMIN_USER.id: ADMIN_USER}
    )


def serialize_app_data(data: ApplicationData):
    return {
        'schema': serialize_constraint(data.schema),
        'expression': serialize_expression(data.expression),
        'users': {
            user.id: serialize_user(user) for user_id, user in data.users.items()
        }
    }
