import secrets
from typing import Annotated
from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRoute
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from stac_fastapi.api.app import StacApi
import os
import json

security = HTTPBasic()

def has_access(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = os.environ.get("BASIC_AUTH_USER").encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = os.environ.get("BASIC_AUTH_PASS").encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def apply_basic_auth(api: StacApi):
    if not os.environ.get("BASIC_AUTH_USER") or not os.environ.get("BASIC_AUTH_PASS"):
        return

    endpoints_json_str = os.environ.get("BASIC_AUTH_ENDPOINTS")
    if endpoints_json_str:
        try:
            endpoints = json.loads(os.environ.get("BASIC_AUTH_ENDPOINTS"))
            parsed_endpoints = []
            for endpoint in endpoints:
                methods = endpoint["method"]
                if isinstance(methods, list):
                    for method in methods:
                        parsed_endpoints.append({"path":endpoint.get("path"), "method":method})
                elif isinstance(methods, str):
                    parsed_endpoints.append({"path":endpoint.get("path"), "method":methods})
                
            api.add_route_dependencies(
                parsed_endpoints,
                [Depends(has_access)]
            )
        except (json.JSONDecodeError, KeyError):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid JSON format for user credentials",
            )
    else:
        app = api.app
        for route in app.routes:
            if isinstance(route, APIRoute):
                for method in route.methods:
                    api.add_route_dependencies(
                        [{"path": route.path, "method": method}],
                        [Depends(has_access)]
                    )