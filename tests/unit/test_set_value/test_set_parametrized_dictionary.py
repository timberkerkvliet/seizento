from unittest import TestCase

from tests.unit.unit_test_client import UnitTestClient


class TestSetParametrizedDictionary(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_with_fixed_object(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        )
        self.test_client.set(
            '/value/test/',
            {
                'fixed': {'een': 1, 'twee': 2, 'drie': 3},
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/test/fixed/<k>}'
                }
            }
        )
        response = self.test_client.get('/value/test/projection')
        self.assertDictEqual(
            response, {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/test/fixed/<k>}'
                }
        )

    def test_reset_value(self):
        self.test_client.set(
            '/schema/test/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    },
                    'alternative': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        )
        self.test_client.set(
            '/value/test/',
            {
                'fixed': {'een': 1, 'twee': 2, 'drie': 3},
                'alternative': {'een': 101, 'twee': 102, 'drie': 103},
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/test/fixed/<k>}'
                }
            }
        )
        self.test_client.set(
            '/value/test/projection/~properties',
            '{/test/alternative/<k>}'
        )
        response = self.test_client.get('/value/test/projection')
        self.assertDictEqual(
            response, {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/test/alternative/<k>}'
                }
        )
