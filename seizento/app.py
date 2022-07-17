from abc import ABC, abstractmethod
from typing import Optional

from seizento.application_data import create_default, ApplicationData
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController


class AppDataOperator(ABC):
    @abstractmethod
    def load(self) -> Optional[ApplicationData]:
        ...

    @abstractmethod
    def save(self, app_data: ApplicationData) -> None:
        ...


class App:
    def __init__(
        self,
        app_secret: str,
        app_data_operator: AppDataOperator
    ):
        data = app_data_operator.load()
        if data is None:
            data = create_default()

        self.resource_controller = ResourceController(
            app_secret=app_secret,
            application_data=data,
            app_data_saver=app_data_operator.save
        )
        self.login_controller = LoginController(
            users=data.users,
            app_secret=app_secret
        )
