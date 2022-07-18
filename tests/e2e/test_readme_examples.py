from tests.e2e.e2e_test_client import E2ETestClient
from tests.unit.test_readme_examples import TestReadmeExample


class E2ETestReadmeExample(TestReadmeExample):
    def setUp(self) -> None:
        self.test_client = E2ETestClient()
        self.test_client.__enter__()

    def tearDown(self) -> None:
        self.test_client.__exit__()
