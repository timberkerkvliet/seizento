import json

from fastapi import FastAPI
from starlette.requests import Request

from seizento.controllers.resource_controller import ResourceController


def get_app(resource_controller: ResourceController) -> FastAPI:
    app = FastAPI()

    @app.get('/{resource_path:path}')
    async def get(resource_path: str):
        return resource_controller.get(resource_path)

    @app.put('/{resource_path:path}')
    async def put(resource_path: str, request: Request):
        return resource_controller.set(resource_path, data=json.loads(await request.body()))

    @app.delete('/{resource_path:path}')
    async def delete(resource_path: str):
        return resource_controller.delete(resource_path)

    return app
