import secrets

from starlette.applications import Starlette

from seizento.expression.struct_literal import StructLiteral
from seizento.schema.constraint import EverythingAllowed
from seizento.schema.schema import Schema
from seizento.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController

from seizento.user import ADMIN_USER

root_schema = Schema(properties={'schema': EverythingAllowed()})
root_expression = StructLiteral(values={})
users = {ADMIN_USER.id: ADMIN_USER}

app_secret = secrets.token_hex(512)

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        root_schema=root_schema,
        root_expression=root_expression,
        users=users,
        app_secret=app_secret,
    ),
    login_controller=LoginController(
        users=users,
        app_secret=app_secret
    )
)

app = Starlette()
app.add_route(
    path='/{rest_of_path:path}',
    route=handler.handle,
    methods=['POST', 'GET', 'PUT', 'DELETE']
)
