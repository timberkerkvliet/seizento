from seizento.application_data import create_default
from seizento.controllers.login_controller import LoginController
from seizento.controllers.resource_controller import ResourceController


class App:
    def __init__(
        self,
        app_secret: str
    ):
        data = create_default()

        self.resource_controller = ResourceController(
            app_secret=app_secret,
            application_data=data
        )
        self.login_controller = LoginController(
            users=data.users,
            app_secret=app_secret
        )
