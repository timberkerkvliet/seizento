from seizento.app_data import AppData
from seizento.schema import Schema
from seizento.serializers.user_serializer import serialize_user, parse_user
from seizento.value import Value


def serialize_app_data(data: AppData):
    return {
        'schema': data.schema.schema,
        'value': data.value.value,
        'users': [serialize_user(user) for user in data.users.values()]
    }


def parse_app_data(data):
    return AppData(
        schema=Schema(data['schema']),
        value=Value(data['value']),
        users={parse_user(user).id: parse_user(user) for user in data['users']}
    )
