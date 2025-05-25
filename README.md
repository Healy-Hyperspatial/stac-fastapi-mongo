# stac-fastapi-mongo

## Mongo backend for the stac-fastapi project built on top of the [sfeos](https://github.com/stac-utils/stac-fastapi-elasticsearch-opensearch) core api library.

[![Downloads](https://static.pepy.tech/badge/stac-fastapi-mongo?color=blue)](https://pepy.tech/project/stac-fastapi-mongo)
  [![GitHub contributors](https://img.shields.io/github/contributors/Healy-Hyperspatial/stac-fastapi-mongo?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/graphs/contributors)
  [![GitHub stars](https://img.shields.io/github/stars/Healy-Hyperspatial/stac-fastapi-mongo.svg?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/stargazers)
  [![GitHub forks](https://img.shields.io/github/forks/Healy-Hyperspatial/stac-fastapi-mongo.svg?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/network/members)
   [![PyPI version](https://img.shields.io/pypi/v/stac-fastapi-mongo.svg?color=blue)](https://pypi.org/project/stac-fastapi-mongo/)
  [![STAC](https://img.shields.io/badge/STAC-1.1.0-blue.svg)](https://github.com/radiantearth/stac-spec/tree/v1.1.0)

<!-- [![Join the chat at https://gitter.im/stac-fastapi-mongo/community](https://badges.gitter.im/stac-fastapi-mongo/community.svg)](https://gitter.im/stac-fastapi-mongo/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) -->

To install from PyPI:

```shell
pip install stac_fastapi.mongo
```

#### For changes, see the [Changelog](CHANGELOG.md)


## Development Environment Setup

To install the classes in your local Python env, run:

```shell
pip install -e .[dev]
```


### Pre-commit

Install [pre-commit](https://pre-commit.com/#install).

Prior to commit, run:

```shell
pre-commit run --all-files
```

## Build stac-fastapi.mongo backend

```shell
docker-compose up mongo
docker-compose build app-mongo
```

## Running Mongo API on localhost:8084

```shell
docker-compose up app-mongo
```

To create a new Collection:

```shell
curl -X "POST" "http://localhost:8084/collections" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "id": "my_collection"
}'
```

Note: this "Collections Transaction" behavior is not part of the STAC API, but may be soon.


## Collection pagination

The collections route handles optional `limit` and `token` parameters. The `links` field that is
returned from the `/collections` route contains a `next` link with the token that can be used to
get the next page of results.

```shell
curl -X "GET" "http://localhost:8084/collections?limit=1&token=example_token"
```

## Testing

```shell
make test
```


## Ingest sample data

```shell
make ingest
```

## Basic Auth

#### Environment Variable Configuration

Basic authentication is an optional feature. You can enable it by setting the environment variable `BASIC_AUTH` as a JSON string.

Example:
```
BASIC_AUTH={"users":[{"username":"user","password":"pass","permissions":"*"}]}
```

### User Permissions Configuration

In order to set endpoints with specific access permissions, you can configure the `users` key with a list of user objects. Each user object should contain the username, password, and their respective permissions.

Example: This example illustrates the configuration for two users: an **admin** user with full permissions (*) and a **reader** user with limited permissions to specific read-only endpoints.
```json
{
    "users": [
        {
            "username": "admin",
            "password": "admin",
            "permissions": "*"
        },
        {
            "username": "reader",
            "password": "reader",
            "permissions": [
                {"path": "/", "method": ["GET"]},
                {"path": "/conformance", "method": ["GET"]},
                {"path": "/collections/{collection_id}/items/{item_id}", "method": ["GET"]},
                {"path": "/search", "method": ["GET", "POST"]},
                {"path": "/collections", "method": ["GET"]},
                {"path": "/collections/{collection_id}", "method": ["GET"]},
                {"path": "/collections/{collection_id}/items", "method": ["GET"]},
                {"path": "/queryables", "method": ["GET"]},
                {"path": "/queryables/collections/{collection_id}/queryables", "method": ["GET"]},
                {"path": "/_mgmt/ping", "method": ["GET"]}
            ]
        }
    ]
}
```


### Public Endpoints Configuration

In order to set endpoints with public access, you can configure the public_endpoints key with a list of endpoint objects. Each endpoint object should specify the path and method of the endpoint.

Example: This example demonstrates the configuration for public endpoints, allowing access without authentication to read-only endpoints.
```json
{
    "public_endpoints": [
        {"path": "/", "method": "GET"},
        {"path": "/conformance", "method": "GET"},
        {"path": "/collections/{collection_id}/items/{item_id}", "method": "GET"},
        {"path": "/search", "method": "GET"},
        {"path": "/search", "method": "POST"},
        {"path": "/collections", "method": "GET"},
        {"path": "/collections/{collection_id}", "method": "GET"},
        {"path": "/collections/{collection_id}/items", "method": "GET"},
        {"path": "/queryables", "method": "GET"},
        {"path": "/queryables/collections/{collection_id}/queryables", "method": "GET"},
        {"path": "/_mgmt/ping", "method": "GET"}
    ],
    "users": [
        {
            "username": "admin",
            "password": "admin",
            "permissions": "*"
        }
    ]
}
```

### Basic Authentication Configurations

See `docker-compose.basic_auth_protected.yml` and `docker-compose.basic_auth_public.yml` for basic authentication configurations.

## Note for read-only databases

If you are using a read-only MongoDB user, the `MONGO_CREATE_INDEXES` environment variable should be set to "false" (as a string and not a boolean) to avoid creating indexes in the database. When this environment variable is not set, the default is to create indexes. See [Github issue #28](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/28)
