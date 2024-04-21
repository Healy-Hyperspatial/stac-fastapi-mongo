"""Basic Authentication Module."""

import hmac
import json
import os
import secrets
from typing import Any, Dict

from fastapi import Depends, HTTPException, Request, status
from fastapi.routing import APIRoute
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

from stac_fastapi.api.app import StacApi

security = HTTPBasic()

_BASIC_AUTH: Dict[str, Any] = {}


def constant_time_compare(actual: bytes, expected: bytes) -> bool:
    """
    Compare two byte strings in constant time to avoid timing attacks.

    This function compares two byte strings byte by byte in a way that
    always takes the same amount of time, regardless of the content of the strings.
    This mitigates timing attacks, where an attacker could infer information
    about the strings being compared based on the time it takes to perform the comparison.

    Args:
        actual (bytes): The first byte string to compare.
        expected (bytes): The second byte string to compare.

    Returns:
        bool: True if the byte strings are equal, False otherwise.
    """
    if len(actual) != len(expected):
        return False
    result = 0
    for x, y in zip(actual, expected):
        result |= x ^ y
    return result == 0


def has_access(
    request: Request, credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    """Check if the provided credentials match the expected \
        username and password stored in environment variables for basic authentication.

    Args:
        request (Request): The FastAPI request object.
        credentials (HTTPBasicCredentials): The HTTP basic authentication credentials.

    Returns:
        str: The username if authentication is successful.

    Raises:
        HTTPException: If authentication fails due to incorrect username or password.
    """
    global _BASIC_AUTH

    users = _BASIC_AUTH.get("users")
    user: Dict[str, Any] = next(
        (u for u in users if u.get("username") == credentials.username), {}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Generate a constant-time comparison HMAC digest of the password
    secret_key = secrets.token_bytes(32)
    expected_digest = hmac.new(
        secret_key, credentials.password.encode("utf-8"), "sha256"
    ).digest()
    actual_digest = hmac.new(
        secret_key, user.get("password", "").encode("utf-8"), "sha256"
    ).digest()

    # Compare the digests in constant time
    if not constant_time_compare(actual_digest, expected_digest):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    permissions = user.get("permissions", [])
    path = request.url.path
    method = request.method

    if permissions == "*":
        return credentials.username
    for permission in permissions:
        if permission["path"] == path and method in permission.get("method", []):
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Insufficient permissions [{path}]",
    )


def apply_basic_auth(api: StacApi) -> None:
    """Apply basic authentication to the provided FastAPI application \
        based on environment variables for username, password, and endpoints.

    Args:
        api (StacApi): The FastAPI application.

    Raises:
        HTTPException: If there are issues with the configuration or format
                       of the environment variables.
    """
    global _BASIC_AUTH

    basic_auth_json_str = os.environ.get("BASIC_AUTH")
    if not basic_auth_json_str:
        print("Basic authentication disabled.")
        return

    try:
        _BASIC_AUTH = json.loads(basic_auth_json_str)
    except json.JSONDecodeError as exception:
        print(f"Invalid JSON format for BASIC_AUTH. {exception=}")
        raise
    public_endpoints = _BASIC_AUTH.get("public_endpoints", [])
    users = _BASIC_AUTH.get("users")
    if not users:
        raise Exception("Invalid JSON format for BASIC_AUTH. Key 'users' undefined.")

    app = api.app
    for route in app.routes:
        if isinstance(route, APIRoute):
            for method in route.methods:
                if {"path": route.path, "method": method} in public_endpoints:
                    continue
                api.add_route_dependencies(
                    [{"path": route.path, "method": method}], [Depends(has_access)]
                )

    print("Basic authentication enabled.")
