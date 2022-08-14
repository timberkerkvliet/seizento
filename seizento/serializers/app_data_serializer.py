from seizento.app_data import AppData
from seizento.serializers.user_serializer import serialize_user, parse_user


def serialize_app_data(data: AppData):
    return {
        'schema': data.schema,
        'value': data.value,
        'users': [serialize_user(user) for user in data.users.values()]
    }


def parse_app_data(data):
    return AppData(
        schema=data['schema'],
        value=data['value'],
        users={parse_user(user).id: parse_user(user) for user in data['users']}
    )
