import os

from starlette.applications import Starlette

from seizento.app import App
from seizento.json_file_operator import JSONFileOperator
from seizento.starlette_request_handler import StarletteRequestHandler


app = App(
    app_secret=os.getenv('APP_SECRET', default='default-secret'),
    app_data_operator=JSONFileOperator()
)

handler = StarletteRequestHandler(app)

starlette_app = Starlette()
starlette_app.add_route(
    path='/{rest_of_path:path}',
    route=handler.handle,
    methods=['POST', 'GET', 'PUT', 'DELETE']
)
