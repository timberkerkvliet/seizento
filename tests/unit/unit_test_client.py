from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController
from seizento.expression.struct_literal import StructLiteral
from seizento.resource import Root
from seizento.schema.constraint import EverythingAllowed
from seizento.schema.schema import Schema
from seizento.schema.types import DataType

from seizento.user import ADMIN_USER


class UnitTestClient:
    def __init__(self):
        root_schema = Schema(types={DataType.OBJECT})
        root_expression = StructLiteral(values={})
        users = {ADMIN_USER.id: ADMIN_USER}

        self.resource_controller = ResourceController(
            users=users,
            app_secret='test-secret',
            root=Root(schema=root_schema, expression=root_expression)
        )
        self.login_controller = LoginController(
            users=users,
            app_secret='test-secret'
        )
        self.token = None

    def login(self, data=None):
        data = data or {
            'user_id': 'admin',
            'password': 'admin'
        }
        self.token = self.login_controller.login(data)

    def get(self, resource: str):
        if self.token is None:
            self.login()
        return self.resource_controller.get(resource=resource, token=self.token)

    def set(self, resource: str, data):
        if self.token is None:
            self.login()
        self.resource_controller.set(resource=resource, data=data, token=self.token)

    def delete(self, resource: str) -> None:
        if self.token is None:
            self.login()
        self.resource_controller.delete(resource=resource, token=self.token)
