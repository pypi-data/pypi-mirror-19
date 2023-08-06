
# Python SDK

[Retsly](https://rets.ly/) Python language SDK. Requires Python@2.7.

## Install

With `pip`
````sh
pip install retsly
````

## Usage

```python
from retsly import Client

retsly = Client("token", "test");

listings = (
  retsly
    .listings()
    .where('bedrooms', '>', '3')
    .getAll()
)
```

## API

All classes are in the `Retsly` namespace. Most methods are chainable.

### Client(token, vendor)

A new instance of `Client` needs an API token. Optionally set the vendor (the MLS data source).

### Client.vendor(vendor)

Sets the vendor to the given value.

### Client.listings([query])

Returns a new `Request` for the Listings resource.

### Client.agents([query])

Returns a new `Request` for the Agents resource.

### Client.offices([query])

Returns a new `Request` for the Offices resource.

### Client.openHouses([query])

Returns a new `Request` for the OpenHouses resource.

### Client.assessments([query])

Returns a new `Request` for the Assessments resource.

### Client.transactions([query])

Returns a new `Request` for the Transactions resource.

### Client.parcels([query])

Returns a new `Request` for the Parcels resource.

### Request.query(query)

Appends the query to the querystring.
```python
request.query({bedrooms: 3})
       .query({bathrooms: {gt: 4});
```

### Request.limit(n)

Alias for `request.query({limit: n})`;

### Request.offset(n)

Alias for `request.query({offset: n})`;

### Request.where(query)

Helper function for building queries, works with different signatures.
```python
request.where(['bedrooms', 'lt', 4])
       .where('livingArea', 'gt', 3000)
       .where('baths', 3)
       .where('garageSpaces 2')
```

### Request.get(id)

Get a single document by its id (`id`).

### Request.getAll()

Get an array of documents.

## License

(The MIT License)

Copyright (c) 2015 Retsly Software Inc <support@rets.ly>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.