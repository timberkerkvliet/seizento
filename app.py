from starlette.applications import Starlette

from seizento.adapters.sqllite_data_tree_store import SQLiteDataTreeStore
from seizento.adapters.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.resource_controller import ResourceController


app = Starlette()
store = SQLiteDataTreeStore(db_path='/data.sql')

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        transaction_factory=lambda: store.get_transaction(),
        token_secret='my-secret'
    )
)

app.add_route(path='/{rest_of_path:path}', route=handler.handle, methods=['GET', 'PUT', 'DELETE'])
