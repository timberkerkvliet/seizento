from seizento.application_data import ApplicationData
from seizento.identifier import Identifier
from seizento.serializers.constraint_serializer import serialize_constraint, parse_constraint
from seizento.serializers.expression_serializer import serialize_expression, parse_expression
from seizento.serializers.user_serializer import serialize_user, parse_user


def serialize_app_data(data: ApplicationData):
    return {
        'schema': serialize_constraint(data.schema),
        'expression': serialize_expression(data.expression),
        'users': [serialize_user(user) for user in data.users.values()]
    }


def parse_app_data(data):
    return ApplicationData(
        schema=parse_constraint(data['schema']),
        expression=parse_expression(data['expression']),
        users={parse_user(user).id: parse_user(user) for user in data['users']}
    )
