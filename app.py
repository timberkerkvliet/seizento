import uuid
from uuid import UUID

from fastapi import FastAPI

from seizento.adapters.in_memory_data_tree_store import InMemoryDataTreeStore
from seizento.adapters.starlette_request_handler import StarletteRequestHandler
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository


app = FastAPI()
store = InMemoryDataTreeStore()

handler = StarletteRequestHandler(
    resource_controller=ResourceController(
        repository_factory=lambda: Repository(store.get_transaction())
    )
)

app.add_route(path='/{rest_of_path:path}', route=handler.handle, methods=['PUT', 'GET', 'DELETE'])
