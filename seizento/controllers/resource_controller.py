from typing import Dict, Any, Callable
from uuid import UUID

from seizento.controllers.evaluation_controller import EvaluationController
from seizento.controllers.exceptions import BadRequest, Unauthorized
from seizento.controllers.expression_controller import ExpressionController
from seizento.controllers.schema_controller import SchemaController
from seizento.path import EMPTY_PATH
from seizento.repository import Repository, DataTreeStoreTransaction, RestrictedDataTreeStoreTransaction, Restricted
from seizento.serializers.path_serializer import parse_path
from seizento.user import AccessRights


class ResourceController:
    def __init__(
        self,
        transaction_factory: Callable[[], DataTreeStoreTransaction]
    ):
        self._transaction_factory = transaction_factory

    def _repository_factory(self) -> Repository:
        return Repository(
            transaction=RestrictedDataTreeStoreTransaction(
                access_rights=AccessRights(read_access={EMPTY_PATH}, write_access={EMPTY_PATH}),
                wrapped=self._transaction_factory()
            )
        )

    @staticmethod
    def _get_controller(resource: str, repository: Repository):
        try:
            resource_path = parse_path(resource)
        except Exception as e:
            raise BadRequest from e

        resource_type = resource_path.first_component.value
        if resource_type == 'schema':
            return SchemaController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'expression':
            return ExpressionController(
                repository=repository,
                path=resource_path.remove_first()
            )
        if resource_type == 'evaluation':
            return EvaluationController(
                repository=repository,
                path=resource_path.remove_first()
            )

        raise BadRequest

    async def get(self, resource: str) -> Dict:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            try:
                return await controller.get()
            except Restricted as e:
                raise Unauthorized from e

    async def set(self, resource: str, data: Any) -> None:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            try:
                await controller.set(data=data)
            except Restricted as e:
                raise Unauthorized from e

    async def delete(self, resource: str) -> None:
        async with self._repository_factory() as repository:
            controller = self._get_controller(resource=resource, repository=repository)

            try:
                await controller.delete()
            except Restricted as e:
                raise Unauthorized from e
