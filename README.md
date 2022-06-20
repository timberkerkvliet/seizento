## Type resource

`/type/{path}`: supports `GET`, `PUT` and `DELETE` methods.

## Expression resource

`/expression/{path}`: supports `GET` and `PUT` and `DELETE` methods.

## Evaluate resource

`/evaluate/{path}`: supports `GET` method.

## User resource

`/user/`: supports `POST` method.

`/user/{user_id}`: supports `GET` and `PUT` and `DELETE` methods.

## Login

`/login`


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
