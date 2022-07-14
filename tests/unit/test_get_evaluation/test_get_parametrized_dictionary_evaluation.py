from unittest import TestCase

from tests.unit.unit_test_client import UnitTestClient


class TestGetParametrizedDictionaryEvaluation(TestCase):
    def setUp(self) -> None:
        self.test_client = UnitTestClient()

    def test_with_fixed_object(self):
        self.test_client.set(
            '/schema/',
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
            '/expression/',
            {
                'fixed': {'een': 1, 'twee': 2, 'drie': 3},
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/fixed/<k>}'
                }
            }
        )
        response = self.test_client.get('/evaluation/projection')
        self.assertEqual(response, {'een': 1, 'twee': 2, 'drie': 3})

    def test_with_fixed_array(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'array',
                        'items': {'type': 'integer'}
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {'type': 'integer'}
                    }
                }
            }
        )
        self.test_client.set(
            '/expression/',
            {
                'fixed': [1, 2, 3],
                'projection': {
                    '*parameter': 'k',
                    '*property': '{k}',
                    '*value': '{/fixed/<k>}'
                }
            }
        )
        response = self.test_client.get('/evaluation/projection')
        self.assertEqual(response, {'0': 1, '1': 2, '2': 3})

    def test_switch_nested_objects(self):
        self.test_client.set(
            '/schema/',
            {
                'type': 'object',
                'properties': {
                    'fixed': {
                        'type': 'object',
                        'additionalProperties': {
                            'type': 'object',
                            'additionalProperties': {'type': 'integer'}
                        }
                    },
                    'projection': {
                        'type': 'object',
                        'additionalProperties': {
                            'type': 'object',
                            'additionalProperties': {'type': 'integer'}
                        }
                    }
                }
            }
        )
        self.test_client.set(
            '/expression/',
            {
                'fixed': {
                    'een': {'a': 1, 'b': 4},
                    'twee': {'a': 2, 'b': 9},
                    'drie': {'a': 0, 'b': 3}
                },
                'projection': {
                    '*parameter': 'y',
                    '*property': '{y}',
                    '*value': {
                        '*parameter': 'x',
                        '*property': '{x}',
                        '*value': '{/fixed/<x>/<y>}'
                    }
                }
            }
        )
        response = self.test_client.get('/evaluation/projection')
        self.assertEqual(
            response,
            {
                'a': {'een': 1, 'twee': 2, 'drie': 0},
                'b': {'een': 4, 'twee': 9, 'drie': 3}
            }
        )
