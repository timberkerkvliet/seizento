from seizento.identifier import Identifier
from seizento.serializers.path_serializer import serialize_path, parse_path
from seizento.user import User, AccessRights, HashedPassword


def serialize_user(user: User):
    return {
        'id': str(user.id),
        'hashed_password': str(user.hashed_password),
        'access_rights': serialize_access_rights(user.access_rights)
    }


def serialize_access_rights(access_rights: AccessRights):
    return {
        'read_access': [serialize_path(path) for path in access_rights.read_access],
        'write_access': [serialize_path(path) for path in access_rights.write_access]
    }


def parse_user(val) -> User:
    return User(
        id=Identifier(val['id']),
        hashed_password=HashedPassword.from_string(val['hashed_password']),
        access_rights=parse_access_rights(val['access_rights'])
    )


def parse_access_rights(val) -> AccessRights:
    return AccessRights(
        read_access={parse_path(path) for path in val['read_access']},
        write_access={parse_path(path) for path in val['write_access']}
    )
