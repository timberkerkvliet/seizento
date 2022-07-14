import secrets

from starlette.applications import Starlette

from seizento.adapters.sqllite_data_tree_store import SQLiteDataTreeStore
from seizento.adapters.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController
from seizento.setup import set_admin

store = SQLiteDataTreeStore(db_path='/db.sql')

app_secret = secrets.token_hex(512)

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        transaction_factory=lambda: store.get_transaction(),
        app_secret=app_secret,
    ),
    login_controller=LoginController(
        transaction_factory=lambda: store.get_transaction(),
        app_secret=app_secret
    )
)


async def on_startup():
    await set_admin(store.get_transaction())

app = Starlette(on_startup=[on_startup])
app.add_route(
    path='/{rest_of_path:path}',
    route=handler.handle,
    methods=['POST', 'GET', 'PUT', 'DELETE']
)
