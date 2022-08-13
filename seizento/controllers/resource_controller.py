from typing import Dict, Any, Callable

import jwt

from seizento.controllers.exceptions import BadRequest, Unauthorized
from seizento.controllers.value_controller import ValueController
from seizento.controllers.schema_controller import SchemaController
from seizento.controllers.user_controller import UserController
from seizento.path import Path
from seizento.application_data import ApplicationData
from seizento.serializers.path_serializer import parse_path
from seizento.serializers.user_serializer import parse_access_rights
from seizento.user import AccessRights


class ResourceController:
    def __init__(
        self,
        app_secret: str,
        application_data: ApplicationData,
        app_data_saver: Callable[[ApplicationData], None]
    ):
        self._app_secret = app_secret
        self._application_data = application_data
        self._app_data_saver = app_data_saver

    def _get_controller(self, resource_path: Path):
        resource_type = resource_path.first_component.value
        if resource_type == 'schema':
            return SchemaController(
                path=resource_path.remove_first(),
                app_data=self._application_data
            )
        if resource_type == 'value':
            return ValueController(
                path=resource_path.remove_first(),
                app_data=self._application_data
            )
        if resource_type == 'user':
            return UserController(
                path=resource_path.remove_first(),
                app_data=self._application_data
            )

        raise BadRequest

    def _get_access_rights(self, token: str) -> AccessRights:
        try:
            return parse_access_rights(
                jwt.decode(jwt=token, key=self._app_secret, algorithms='HS256')
            )
        except Exception as e:
            raise Unauthorized

    @staticmethod
    def _get_resource_path(resource: str) -> Path:
        try:
            return parse_path(resource)
        except Exception as e:
            raise BadRequest from e

    def get(self, resource: str, token: str) -> Dict:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_read(resource_path):
            raise Unauthorized

        controller = self._get_controller(resource_path=resource_path)
        return controller.get()

    def set(self, resource: str, data: Any, token: str) -> None:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_write(resource_path):
            raise Unauthorized

        controller = self._get_controller(resource_path=resource_path)
        controller.set(data)

        self._app_data_saver(self._application_data)

    def delete(self, resource: str, token: str) -> None:
        access_rights = self._get_access_rights(token)
        resource_path = self._get_resource_path(resource)

        if not access_rights.can_write(resource_path):
            raise Unauthorized

        controller = self._get_controller(resource_path=resource_path)
        controller.delete()

        self._app_data_saver(self._application_data)
