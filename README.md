## What does seizento do?

Seizento should do two things well:
* It stores JSON data conforming to a JSON schema
* It enables JSON projections by an expression language

## The products example

### Setting literals

Suppose that by a PUT request to `/schema/` we set the following schema (using the defined standard at https://json-schema.org/):

```
{
    "type": "object",
    "properties: {
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "on_stock": {"type": "boolean"}
                 }
            }
        }
    }
    
}
```

In words: under the property `products` we have a list of products with the properties `id`, `name` and `on_stock`.
Then data for this schema can be set with a PUT request to `/expression/`:

```
{
    "products": [
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
}
```

We are using the `expression` endpoint, but the data we are submitting is just a literal value.
If we get the evaluation of the expression by a `GET` request on `/evaluation/`, 
we get exactly the same data back.

### Creating a projection

Now for something more interesting, suppose that someone else needs the data in the form of a map from product names to stock.
Suppose we extend schema by a PUT request to  `/schema/stock` with payload:

```
{
    "type": "object",
    "additionalProperties": {
        {"type": "boolean"}
    }
}
```

This creates a `stock` property in addition to the already existing `products` property in the root schema.

Then we can set an expression to define our desired values with a PUT request to `/expression/stock`:

```
{
    "*parameter": "k",
    "*property": "{products/<k>/name}"
    "*value": "{products/<k>/on_stock}"
}
```

And by sending a GET request to `/evaluation/stock` we get it evaluated:

```
{
    "Boring product": true
    "Fancy product": false
}
```
