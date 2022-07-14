from starlette.requests import Request
from starlette.responses import JSONResponse

from seizento.controllers.exceptions import NotFound, BadRequest, Forbidden
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController


class StarletteRequestHandler:
    def __init__(
        self,
        resource_controller: ResourceController,
        login_controller: LoginController
    ):
        self._resource_controller = resource_controller
        self._login_controller = login_controller

    async def handle(self, request: Request) -> JSONResponse:
        resource = request.url.path
        try:
            if request.method == 'POST' and resource == '/login':
                return JSONResponse(await self._login_controller.login(data=await request.json()))

            auth = request.headers.get('Authorization')

            if auth is None or auth[:7] != 'Bearer ':
                return JSONResponse(status_code=401, content='')

            token = auth[7:]

            if request.method == 'GET':
                return JSONResponse(
                    await self._resource_controller.get(resource=resource, token=token)
                )
            if request.method == 'PUT':
                data = await request.json()
                return JSONResponse(
                    await self._resource_controller.set(resource=resource, data=data, token=token)
                )
            if request.method == 'DELETE':
                return JSONResponse(
                    await self._resource_controller.delete(resource=resource, token=token)
                )
            return JSONResponse(content='', status_code=405)
        except NotFound as e:
            return JSONResponse(content=str(e), status_code=404)
        except BadRequest as e:
            return JSONResponse(content=str(e), status_code=400)
        except Forbidden as e:
            return JSONResponse(content=str(e), status_code=403)