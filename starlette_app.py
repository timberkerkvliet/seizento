import secrets

from starlette.applications import Starlette

from seizento.app import App
from seizento.json_file_operator import JSONFileOperator
from seizento.starlette_request_handler import StarletteRequestHandler


app = App(
    app_secret=secrets.token_hex(512),
    app_data_operator=JSONFileOperator('/app-data/data.json')
)

handler = StarletteRequestHandler(app)

starlette_app = Starlette()
starlette_app.add_route(
    path='/{rest_of_path:path}',
    route=handler.handle,
    methods=['POST', 'GET', 'PUT', 'DELETE']
)
