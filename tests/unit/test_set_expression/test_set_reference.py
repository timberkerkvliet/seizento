from unittest import IsolatedAsyncioTestCase

from seizento.controllers.exceptions import Forbidden, NotFound
from tests.unit.unit_test_client import UnitTestClient


class TestSetReference(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_client = UnitTestClient()

    async def test_reference_with_wrong_type(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'string'}
                }
            }
        )
        self.test_client.set('/expression', {'a': 5})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression/b', '{/a}')

    async def test_self_reference(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        with self.assertRaises(Forbidden):
            self.test_client.set('/expression', ['{/0}'])

    async def test_self_reference_did_not_change_anything(self):
        self.test_client.set('/schema/', {'type': 'array', 'items': {'type': 'integer'}})

        self.test_client.set('/expression', [1])

        try:
            self.test_client.set('/expression', ['{/0}'])
        except Forbidden:
            pass

        response = self.test_client.get('/expression')

        self.assertEqual(response, [1])
