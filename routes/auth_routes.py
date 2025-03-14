"""
This file defines the authentication routes for the API using FastAPI.

It includes the `/login` endpoint that handles user login requests. Users must provide a
username (18 characters) and a password (15 characters) to authenticate. The authentication
is managed by the `AuthServices` class, which verifies the credentials and returns a response
containing either an access token or an error message.

The `APIRouter` is used to register the login route, and the `JSONResponse` is used to send
responses with the appropriate status code and data.

Endpoints:
    POST /login: Authenticates a user by verifying their username and password.
"""

from typing import Annotated
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from services.auth_services import AuthServices

auth_routes = APIRouter()
auth = AuthServices()


@auth_routes.post("/login")
async def login(
    username: Annotated[str, Body(max_length=18, min_length=18)],
    password: Annotated[str, Body(max_length=15, min_length=15)],
) -> JSONResponse:
    """
    Handles user login requests.

    Args:
        username (Annotated[str]): The username of the user. Must be exactly 18 characters.
        password (Annotated[str]): The password of the user. Must be exactly 15 characters.

    Returns:
        JSONResponse: A response with the login result.
                      - On success: Status code 200 with user information or token.
                      - On failure: Status code and error details based on `AuthServices`.

    Example:
        Request Body:
        {
            "username": "user_example_12345",
            "password": "secure_password"
        }

        Response:
        {
            "token": "access token",
            "student_data": { ... }  # Student details
        }
    """
    return JSONResponse(
        status_code=200,
        content=await auth.login(username, password)
    )
