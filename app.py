import secrets

from starlette.applications import Starlette

from seizento.adapters.sqllite_data_tree_store import SQLiteDataTreeStore
from seizento.adapters.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository
from seizento.user import ADMIN_USER

store = SQLiteDataTreeStore(db_path='/db.sql')


async def set_admin():
    repository = Repository(transaction=store.get_transaction())
    async with repository:
        await repository.set_user(ADMIN_USER)

app = Starlette(on_startup=[set_admin])

app_secret = secrets.token_hex(512)

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        transaction_factory=lambda: store.get_transaction(),
        app_secret=app_secret
    ),
    login_controller=LoginController(
        transaction_factory=lambda: store.get_transaction(),
        app_secret=app_secret
    )
)

app.add_route(path='/{rest_of_path:path}', route=handler.handle, methods=['POST', 'GET', 'PUT', 'DELETE'])
