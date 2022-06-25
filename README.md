## What does seizento do?

Seizento should do two things well:
* It stores JSON data conforming to a JSON schema
* It enables JSON projections by an expression language

Let's illustrate this with an example.

Suppose that by a GET request to `/schema/products` we find that the defined schema (using the defined standard at https://json-schema.org/) is:

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

Then data for this schema can be set with a PUT request to `/expression/products`:

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

We are using the `expression` endpoint, but the data we are submitting is just a literal (array) value.
If we get the evaluation of the expression by a `GET` request on `/evaluation/products`, 
we get exactly the same data back.

Now for something more interesting, suppose that someone else needs the data in the form of a map from product names to stock.
Suppose that by a GET request to  `/schema/stock` we find that a schema is defined as follows:

```
{
    "type": "object",
    "additionalProperties": {
        {"type": "boolean"}
    }
}
```

Then we can set an expression to define our desired values with a PUT request to `/expression/stock`:

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