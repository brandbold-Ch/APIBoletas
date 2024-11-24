from services.history_services import HistoryServices
from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from utils.token import CustomHTTPBearer
from fastapi.requests import Request
from typing import Annotated

history_routes = APIRouter()
history = HistoryServices()
bearer = CustomHTTPBearer()


@history_routes.get("/", dependencies=[Depends(bearer)])
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
        content=history.get_histories(enrollment, rank, partial).to_repr()
    )


@history_routes.get("/semiannual", dependencies=[Depends(bearer)])
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
        content=history.get_histories(enrollment, rank, 6).to_repr()
    )
