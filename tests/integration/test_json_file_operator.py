from unittest import TestCase

from seizento.application_data import create_default, ApplicationData
from seizento.value.array_literal import ArrayLiteral
from seizento.value.primitive_literal import PrimitiveLiteral
from seizento.value.struct_literal import StructLiteral
from seizento.json_file_operator import JSONFileOperator
from seizento.schema import Schema
from seizento.schema.types import DataType
from seizento.user import ADMIN_USER


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
        app_data = ApplicationData(
            schema=Schema(
                types={DataType.OBJECT},
                properties={
                    'a': Schema(types={DataType.OBJECT, DataType.INTEGER}),
                    'b': Schema(types={DataType.ARRAY}, items=Schema(types={DataType.INTEGER}))
                }
            ),
            expression=StructLiteral(
                values={
                    'a': PrimitiveLiteral(900),
                    'b': ArrayLiteral(values=[PrimitiveLiteral(1), PrimitiveLiteral(2)])
                }
            ),
            users={ADMIN_USER.id: ADMIN_USER}
        )

        operator.save(app_data)
        result = operator.load()

        self.assertEqual(app_data, result)
