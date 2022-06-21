## Type resource

`/type/{path}`: supports `GET`, `PUT` and `DELETE` methods.

## Expression resource

`/expression/{path}`: supports `GET` and `PUT` and `DELETE` methods.

## Evaluation resource

`/evaluation/{path}`: supports `GET` method.


Supports only `GET` method.

## Data types

* Array: unordered list of elements with a fixed schema
* Struct: composite of different schemas, all identified by a name
* Dictionary: elements identified by a key, all available keys are known
* Function: parametrized type
* String
* Encrypted string: string with metadata about the encryption
* Bool
* Integer
* Float