# stac-fastapi-mongo

<!-- markdownlint-disable MD033 MD041 -->

<p align="left">
  <img src="assets/stac-fastapi-mongo.png" width=560>
</p>


MongoDB backend for the [stac-fastapi](https://github.com/stac-utils/stac-fastapi) project built on top of the [sfeos](https://github.com/stac-utils/stac-fastapi-elasticsearch-opensearch) core API library.

[![Downloads](https://static.pepy.tech/badge/stac-fastapi-mongo?color=blue)](https://pepy.tech/project/stac-fastapi-mongo)
[![GitHub contributors](https://img.shields.io/github/contributors/Healy-Hyperspatial/stac-fastapi-mongo?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/graphs/contributors)
[![GitHub stars](https://img.shields.io/github/stars/Healy-Hyperspatial/stac-fastapi-mongo.svg?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Healy-Hyperspatial/stac-fastapi-mongo.svg?color=blue)](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/network/members)
[![PyPI version](https://img.shields.io/pypi/v/stac-fastapi-mongo.svg?color=blue)](https://pypi.org/project/stac-fastapi-mongo/)
[![STAC](https://img.shields.io/badge/STAC-1.1.0-blue.svg)](https://github.com/radiantearth/stac-spec/tree/v1.1.0)

<!-- [![Join the chat at https://gitter.im/stac-fastapi-mongo/community](https://badges.gitter.im/stac-fastapi-mongo/community.svg)](https://gitter.im/stac-fastapi-mongo/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) -->

## Technologies

This project is built on the following technologies: STAC, stac-fastapi, FastAPI, MongoDB, Python

<p align="left">
  <a href="https://stacspec.org/"><img src="https://raw.githubusercontent.com/stac-utils/stac-fastapi-elasticsearch-opensearch/refs/heads/main/assets/STAC-01.png" alt="STAC" height="100" hspace="10"></a>
  <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/stac-utils/stac-fastapi-elasticsearch-opensearch/refs/heads/main/assets/python.png" alt="Python" height="80" hspace="10"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://raw.githubusercontent.com/stac-utils/stac-fastapi-elasticsearch-opensearch/refs/heads/main/assets/fastapi.svg" alt="FastAPI" height="80" hspace="10"></a>
  <a href="https://www.mongodb.com/"><img src="assets/mongodb.webp" alt="MongoDB" height="80" hspace="10"></a>
</p>


## Table of Contents

- [Installation](#installation)
- [Development](#development)
  - [Development Environment Setup](#development-environment-setup)
  - [Pre-commit](#pre-commit)
- [Running the API](#running-the-api)
  - [Build and Run](#build-and-run)
  - [Creating Collections](#creating-collections)
  - [Collection Pagination](#collection-pagination)
- [Testing](#testing)
- [Sample Data](#sample-data)
- [Authentication](#authentication)
  - [Environment Variable Configuration](#environment-variable-configuration)
  - [Authentication Configuration](#authentication-configuration)
  - [Examples](#examples)
    - [Admin-only Authentication](#admin-only-authentication)
    - [Public Endpoints with Admin Authentication](#public-endpoints-with-admin-authentication)
    - [Multi-user Authentication](#multi-user-authentication)
- [Read-Only Databases](#note-for-read-only-databases)
- [Contributing](#contributing)
- [Changelog](#changelog)

## Installation

To install from PyPI:

```shell
pip install stac_fastapi.mongo
```

## Development

### Development Environment Setup

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

## Running the API

### Build and Run

Build the MongoDB backend:

```shell
docker-compose up mongo
docker-compose build app-mongo
```

Run the MongoDB API on localhost:8084:

```shell
docker-compose up app-mongo
```

### Creating Collections

To create a new Collection:

```shell
curl -X "POST" "http://localhost:8084/collections" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "id": "my_collection"
}'
```

Note: this "Collections Transaction" behavior is not part of the STAC API, but may be soon.

### Collection Pagination

The collections route handles optional `limit` and `token` parameters. The `links` field that is
returned from the `/collections` route contains a `next` link with the token that can be used to
get the next page of results.

```shell
curl -X "GET" "http://localhost:8084/collections?limit=1&token=example_token"
```

## Testing

Run the test suite:

```shell
make test
```

## Sample Data

Ingest sample data:

```shell
make ingest
```

## Authentication

### Environment Variable Configuration

Basic authentication is an optional feature. You can enable it by setting the environment variable `STAC_FASTAPI_ROUTE_DEPENDENCIES` as a JSON string.

Example:
```
STAC_FASTAPI_ROUTE_DEPENDENCIES=[{"routes":[{"method":"*","path":"*"}],"dependencies":[{"method":"stac_fastapi.core.models.basic_auth.BasicAuth","kwargs":{"credentials":[{"username":"admin","password":"admin"}]}}]}]
```

### Authentication Configuration

The `STAC_FASTAPI_ROUTE_DEPENDENCIES` environment variable allows you to configure different levels of authentication for different routes. The configuration is a JSON array of objects, each with two properties:

1. `routes`: An array of route objects, each with `method` and `path` properties
2. `dependencies`: An array of dependency objects, each with `method` and `kwargs` properties

#### Examples

##### Admin-only Authentication

This example configures all routes to require admin authentication:

```json
[
    {
        "routes": [
            {
                "method": "*",
                "path": "*"
            }
        ],
        "dependencies": [
            {
                "method": "stac_fastapi.core.models.basic_auth.BasicAuth",
                "kwargs": {
                    "credentials": [
                        {
                            "username": "admin",
                            "password": "admin"
                        }
                    ]
                }
            }
        ]
    }
]
```

##### Public Endpoints with Admin Authentication

This example makes specific endpoints public while requiring admin authentication for all others:

```json
[
    {
        "routes": [
            {
                "method": "*",
                "path": "*"
            }
        ],
        "dependencies": [
            {
                "method": "stac_fastapi.core.models.basic_auth.BasicAuth",
                "kwargs": {
                    "credentials": [
                        {
                            "username": "admin",
                            "password": "admin"
                        }
                    ]
                }
            }
        ]
    },
    {
        "routes": [
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
        ],
        "dependencies": []
    }
]
```

##### Multi-user Authentication

This example configures admin authentication for all routes, with a separate reader user that can access specific read-only endpoints:

```json
[
    {
        "routes": [
            {
                "method": "*",
                "path": "*"
            }
        ],
        "dependencies": [
            {
                "method": "stac_fastapi.core.models.basic_auth.BasicAuth",
                "kwargs": {
                    "credentials": [
                        {
                            "username": "admin",
                            "password": "admin"
                        }
                    ]
                }
            }
        ]
    },
    {
        "routes": [
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
        ],
        "dependencies": [
            {
                "method": "stac_fastapi.core.models.basic_auth.BasicAuth",
                "kwargs": {
                    "credentials": [
                        {
                            "username": "reader",
                            "password": "reader"
                        }
                    ]
                }
            }
        ]
    }
]
```

> **Note**: The older `BASIC_AUTH` environment variable format is deprecated and will be removed in a future release.

## Note for Read-Only Databases

If you are using a read-only MongoDB user, the `MONGO_CREATE_INDEXES` environment variable should be set to "false" (as a string and not a boolean) to avoid creating indexes in the database. When this environment variable is not set, the default is to create indexes. See [GitHub issue #28](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/28)

## Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the repository** - Create your own fork of the project
2. **Create a feature branch** - `git checkout -b feature/your-feature-name`
3. **Commit your changes** - Make sure to write clear, concise commit messages
4. **Push to your branch** - `git push origin feature/your-feature-name`
5. **Open a Pull Request** - Describe your changes in detail

### Development Guidelines

- Follow the existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Make sure all tests pass before submitting a PR

### Reporting Issues

If you find a bug or have a feature request, please open an issue on the [GitHub repository](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues).

## Changelog

For changes, see the [Changelog](CHANGELOG.md)
