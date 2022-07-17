from seizento.app import App


class UnitTestClient:
    def __init__(self):
        self.app = App(app_secret='test-secret')
        self.token = None

    def login(self, data=None):
        data = data or {
            'user_id': 'admin',
            'password': 'admin'
        }
        self.token = self.app.login_controller.login(data)

    def get(self, resource: str):
        if self.token is None:
            self.login()
        return self.app.resource_controller.get(resource=resource, token=self.token)

    def set(self, resource: str, data):
        if self.token is None:
            self.login()
        self.app.resource_controller.set(resource=resource, data=data, token=self.token)

    def delete(self, resource: str) -> None:
        if self.token is None:
            self.login()
        self.app.resource_controller.delete(resource=resource, token=self.token)
