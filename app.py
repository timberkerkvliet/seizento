import secrets

from starlette.applications import Starlette

from seizento.application_data import create_default
from seizento.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController

app_secret = secrets.token_hex(512)
data = create_default()

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        application_data=data,
        app_secret=app_secret,
    ),
    login_controller=LoginController(
        users=data.users,
        app_secret=app_secret
    )
)

app = Starlette()
app.add_route(
    path='/{rest_of_path:path}',
    route=handler.handle,
    methods=['POST', 'GET', 'PUT', 'DELETE']
)
