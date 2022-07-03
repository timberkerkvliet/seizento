from uuid import UUID

from fastapi import FastAPI

from seizento.adapters.starlette_adapter import FastAPIRequestHandler
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository
from tests.test_interface.test_client import FakeDataTreeStore

app = FastAPI()
store = FakeDataTreeStore()

handler = FastAPIRequestHandler(
    resource_controller=ResourceController(
        repository_factory=lambda: Repository(store.get_transaction()),
        user_id=UUID()
    )
)

app.add_route(path='/', route=handler.handle)
