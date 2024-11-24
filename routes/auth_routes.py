from services.auth_services import AuthServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body
from typing import Annotated

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
        content=auth.login(username, password)
    )
