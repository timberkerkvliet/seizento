from uuid import UUID

from fastapi import FastAPI

from seizento.adapters.fake_data_tree_store import FakeDataTreeStore
from seizento.adapters.starlette_adapter import StarletteAdapter
from seizento.controllers.resource_controller import ResourceController
from seizento.repository import Repository


app = FastAPI()
store = FakeDataTreeStore()

handler = StarletteAdapter(
    resource_controller=ResourceController(
        repository_factory=lambda: Repository(store.get_transaction()),
        user_id=UUID()
    )
)

app.add_route(path='/', route=handler.handle)
