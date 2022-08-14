from unittest import TestCase

from seizento.app_data import create_default, AppData
from seizento.json_file_operator import JSONFileOperator
from seizento.schema import Schema
from seizento.user import ADMIN_USER
from seizento.value import Value


class TestJsonFileOperator(TestCase):
    def test_non_existing_file(self):
        operator = JSONFileOperator('some-non-existing-file.json')
        self.assertIsNone(operator.load())

    def test_default(self):
        operator = JSONFileOperator('data.json')
        app_data = create_default()

        operator.save(app_data)
        result = operator.load()

        self.assertEqual(app_data, result)

    def test_complex(self):
        operator = JSONFileOperator('data.json')
        app_data = AppData(
            schema=Schema(
                schema={
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'string'}
                    }
                }
            ),
            value=Value({'a': 'some valuee'}),
            users={ADMIN_USER.id: ADMIN_USER}
        )

        operator.save(app_data)
        result = operator.load()

        self.assertEqual(app_data, result)
