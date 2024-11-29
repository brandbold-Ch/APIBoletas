"""
This file defines the route for retrieving student data from the API based on a student's enrollment ID.

It includes a single endpoint:

1. `/students/{enrollment}` - Retrieves the student data for the student associated with the provided enrollment ID.
   The enrollment ID must be exactly 15 characters long. The request is authenticated using a Bearer token
   and the `authenticate` decorator ensures the user is properly authenticated before accessing the data.

The `StudentServices` class handles the logic for retrieving student data, and the `CustomHTTPBearer` class
is used to ensure that a valid Bearer token is included in the request headers.

Dependencies:
    - Bearer Token Authentication: Required for this route.
    - A valid enrollment ID that is exactly 15 characters long.

Example Request:
    - GET /students/{enrollment}

Example Response:
    - On success: Status code 200 with student data.
    - On failure: Status code with error message.
"""

from typing import Annotated
from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from services.student_services import StudentServices
from decorators.authenticator import authenticate
from utils.token_tools import CustomHTTPBearer

student_routes = APIRouter()
student = StudentServices()
bearer = CustomHTTPBearer()


@student_routes.get("/{enrollment}", dependencies=[Depends(bearer)])
@authenticate
async def get_student(
        request: Request,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)]
) -> JSONResponse:
    """
    Retrieve the student data based on the provided enrollment ID.

    Args:
        request (Request): The HTTP request object, automatically passed by FastAPI.
        enrollment (Annotated[str]): The student's enrollment ID. Must be exactly 15 characters.

    Returns:
        JSONResponse: A response containing the student's data.
                      - On success: Status code 200 with the student data in the response.
                      - On failure: Status code and error details.

    Authentication:
        Requires a valid bearer token in the `Authorization` header.
        The `authenticate` decorator ensures that the user is properly authenticated.

    Example:
        Request:
        GET students/{enrollment}

        Response on success:
        {...}

        Response on failure:
        {
            "status": "Http argument",
            "message": "Custom exception"
        }
    """
    return JSONResponse(status_code=200, content=student.get_student(enrollment).to_repr())
