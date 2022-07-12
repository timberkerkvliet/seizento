from __future__ import annotations

from enum import Enum


class DataType(Enum):
    NULL = 'null'
    STRING = 'string'
    BOOL = 'boolean'
    FLOAT = 'number'
    INTEGER = 'integer'
    OBJECT = 'object'
    ARRAY = 'array'


ALL_TYPES = {
    DataType.NULL,
    DataType.STRING,
    DataType.BOOL,
    DataType.FLOAT,
    DataType.INTEGER,
    DataType.OBJECT,
    DataType.ARRAY
}
