`/schemas/{my-config}`

Access the schema of your configuration

`/expressions/{my-config}`

Access expressions

Use `PUT` on `/literals/{my-config}`

Access expressions

Use `/parsed/{my-config}` to get the values for your configuration. Only `GET` operation is supported.

## Data types

* Array: unordered list of elements with a fixed schema
* Struct: composite of different schemas, all identified by a name
* Dictionary: elements identified by a key, all available keys are known
* Function: elements identified by a key
* String
* Bool
* Integer
* Float
