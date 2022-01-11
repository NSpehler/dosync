# Dosync

Building an 2-way sync against a REST API in Python for a coding challenge. It uses MongoDB and MongoEngine as ORM.

## Docs

The full instructions are available [here](docs/instructions.md).

## Installation

To use this package, you need to run Python 3.7 or newer.

Start by installing the required packages from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

Then, make sure to add the API endpoint in the `.env` file:

```env
API_URL=https://SECRET.mockapi.io/api/v1
```

Last, start your local MongoDB instance:

```sh
mongod
```

## Usage

You can run Dosync with the following command:

```sh
python3 start.py
```

If you need to force the syncronization again, you can remove the attributes in the `metadata` collection on your MongoDB instance.

## Notes

### Nested `adsets`, `keywords` and `ads`

The decision was made to nest `adsets`, `keywords` and `ads` inside a unique `campaigns` collection in MongoDB.

An alternative architecture would be to create separate `adsets`, `keywords` and `ads` collections, mainly based on the use case and performance needs.

### Store last sync timestamps in database

We only update campaigns that have been recently updated to avoid making unnecessary API calls to the remote API. To do so, we store and update the latest sync timestamps in a `metadata` collection in our database.

### Rate limiting from MockAPI.io

To avoid rate limiting from MockAPI.io, a 1-second delay was added before any API request.

### Integer to string conversion on MockAPI.io

We're facing an issue where MockAPI.io seems to be converting all integers to strings, so the updated data is never identical to the original one.

## Improvement ideas

- Batch update in database to reduce number of write operations
- Add more unit tests for improved coverage

## Meta

Nicolas Spehler – [@NSpehler](https://twitter.com/NSpehler)
