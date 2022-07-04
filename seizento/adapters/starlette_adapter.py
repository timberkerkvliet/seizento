import json

from starlette.requests import Request
from starlette.responses import Response

from seizento.controllers.exceptions import NotFound, BadRequest, Forbidden
from seizento.controllers.resource_controller import ResourceController


class StarletteAdapter:
    def __init__(self, resource_controller: ResourceController):
        self._resource_controller = resource_controller

    async def handle(self, request: Request) -> Response:
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
                return Response(status_code=405)
        except NotFound:
            return Response(status_code=404)
        except BadRequest:
            return Response(status_code=400)
        except Forbidden:
            return Response(status_code=401)

        return Response(json.dumps(result))
