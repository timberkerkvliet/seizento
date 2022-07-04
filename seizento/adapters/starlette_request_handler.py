import json

from starlette.requests import Request
from starlette.responses import JSONResponse

from seizento.controllers.exceptions import NotFound, BadRequest, Forbidden
from seizento.controllers.resource_controller import ResourceController


class StarletteRequestHandler:
    def __init__(self, resource_controller: ResourceController):
        self._resource_controller = resource_controller

    async def handle(self, request: Request) -> JSONResponse:
        resource = request.url.path
        try:
            if request.method == 'GET':
                result = await self._resource_controller.get(resource=resource)
            elif request.method == 'PUT':
                data = await request.json()
                result = await self._resource_controller.set(resource=resource, data=data)
            elif request.method == 'DELETE':
                result = await self._resource_controller.delete(resource=resource)
            else:
                return JSONResponse(content='', status_code=405)
        except NotFound as e:
            return JSONResponse(content=str(e), status_code=404)
        except BadRequest as e:
            return JSONResponse(content=str(e), status_code=400)
        except Forbidden as e:
            return JSONResponse(content=str(e), status_code=403)

        return JSONResponse(content=result, status_code=200)
