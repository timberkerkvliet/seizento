## What does seizento do?

### It stores JSON data conforming to a defined schema

Suppose that by a GET request to `/schema/products` we find that the defined schema is:

```
{
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "on_stock: {"type: "boolean"}
        }
}
```

Then data for this schema can be set with a PUT request to `/expression/product`

```
[
    {
        "id": 1,
        "name": "Boring product",
        "on_stock": true
    },
    {
        "id": 2,
        "name": "Fancy product",
        "on_stock": false
    }
]
```

### It enables JSON projections

Now suppose that someone else needs the data in the form of a map from product names to stock.
Suppose that by a GET request to  `/schema/stock` we find that a schema is defined as follows:

```
{
    "type": "object",
    "additionalProperties": {
        {"type": "boolean"}
    }
}
```

Then we can set the value with a PUT request to `/expression/stock`

```
{  
    "{products/<k>/name}": "{products/<k>/stock}"
}
```

And by sending a GET request to `/evaluation/stock` we get it evaluated:

```
{
    "Boring product": true
    "Fancy product": false
}
```