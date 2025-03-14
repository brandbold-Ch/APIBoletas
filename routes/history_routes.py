"""
This file defines the routes for retrieving academic history records of students in the API.

It includes two endpoints:

1. `/histories/` - Retrieves detailed academic history records for a student based on their
   enrollment ID, academic rank, and specific partial exam period (1 to 3).

2. `/histories/semiannual/` - Retrieves semiannual academic history records for a student
   based on their enrollment ID and academic rank.

The routes use Bearer token authentication to ensure that only authorized users can access
the data. The `CustomHTTPBearer` is used to handle the authentication process.

The `HistoryServices` class is responsible for retrieving and formatting the academic history
data, which is then returned as a `JSONResponse`.

Dependencies:
    - Bearer Token Authentication: Required for both routes.
    - Valid enrollment ID, rank, and partial exam period (for `/histories/`) or rank (for
      `/histories/semiannual/`).

Example Requests:
    - GET {enrollment}/histories/?rank=3&partial=2
    - GET {enrollment}/histories/semiannual/?rank=3
"""

from typing import Annotated
from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from utils.token_tools import CustomHTTPBearer
from services.history_services import HistoryServices
from decorators.authenticator import authenticate

history_routes = APIRouter()
history = HistoryServices()
bearer = CustomHTTPBearer()


@history_routes.get("/", dependencies=[Depends(bearer)])
@authenticate
async def get_academic_histories(
        request: Request,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        rank: Annotated[int, Query(ge=1, le=6)],
        partial: Annotated[int, Query(ge=1, le=3)],
) -> JSONResponse:
    """
    Retrieve academic history records for a student.

    Args:
        request (Request): The HTTP request object, automatically passed by FastAPI.
        enrollment (Annotated[str]): The student's enrollment ID. Must be exactly 15 characters.
        rank (Annotated[int]): The academic rank of the student (1 to 6).
        partial (Annotated[int]): The specific academic period (1 to 3).

    Returns:
        JSONResponse: A response containing the student's academic history.
                      - On success: Status code 200 with the academic history data.
                      - On failure: Status code and error details.

    Authentication:
        Requires a valid bearer token in the `Authorization` header.

    Example:
        Request:
        GET {enrollment}/histories/?rank=3&partial=2

        Response on success:
        {...}

        Response on failure:
        {
            "status": "Http argument",
            "message": "Custom exception"
        }
    """
    return JSONResponse(
        status_code=200,
        content=await history.get_histories(enrollment, partial, str(rank))
    )


@history_routes.get("/semiannual", dependencies=[Depends(bearer)])
@authenticate
async def get_semiannual_academic_histories(
        request: Request,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        rank: Annotated[int, Query(ge=1, le=6)],
) -> JSONResponse:
    """
    Retrieve semiannual academic history records for a student.

    Args:
        request (Request): The HTTP request object, automatically passed by FastAPI.
        enrollment (Annotated[str]): The student's enrollment ID. Must be exactly 15 characters.
        rank (Annotated[int]): The academic rank of the student (1 to 6).

    Returns:
        JSONResponse: A response containing the semiannual academic history.
                      - On success: Status code 200 with the academic history data.
                      - On failure: Status code and error details.

    Authentication:
        Requires a valid bearer token in the `Authorization` header.

    Example:
        Request:
        GET {enrollment}/histories/semiannual/?rank=3

        Response on success:
        {...}

        Response on failure:
        {
            "status": "Http argument",
            "message": "Custom exception"
        }
    """
    return JSONResponse(
        status_code=200,
        content=await history.get_histories(enrollment, 6, rank)
    )
