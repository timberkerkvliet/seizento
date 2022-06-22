## What does seizento do?

### It stores JSON data validated against a schema

First, a schema must be set, by sending a PUT request to `/schema/products`:

```
{
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "on_stock: {"type: "bool"}
    }
}
```

And then, data for this schema can be set with a PUT request to `/expression/product`

```
{
    "id": 1,
    "name": "My product",
    "on_stock": True
}
```

### It transforms JSON data

Now suppose that we set a different schema at `/schema/stock`

```
{
    "type": "object",
    "additionalProperties": {
        {"type": "integer"}
    }
}
```

Then we can set the value with a PUT request to `/expression/stock`

```
{
    '{product/name}': '{product/stock}'
}
```

And by sending a GET request to `/evaluation/stock` we get it evaluated:

```
{
    "My Product": True
}
```