from starlette.applications import Starlette

from seizento.adapters.sqllite_data_tree_store import SQLiteDataTreeStore
from seizento.adapters.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository


app = Starlette()
store = SQLiteDataTreeStore(db_path='/data.sql')

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        repository_factory=lambda: Repository(store.get_transaction())
    )
)

app.add_route(path='/{rest_of_path:path}', route=handler.handle, methods=['GET', 'PUT', 'DELETE'])
