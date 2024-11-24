from fastapi import APIRouter, Path, Query, Depends, BackgroundTasks
from decorators.authenticator import authenticate
from services.load_services import LoadServices
from fastapi.responses import JSONResponse
from utils.token import CustomHTTPBearer
from utils.tasks import check_student
from fastapi.requests import Request
from typing import Annotated

load_routes = APIRouter()
load = LoadServices()
bearer = CustomHTTPBearer()


@load_routes.get("/", dependencies=[Depends(bearer)])
@authenticate
async def get_academic_loads(
        request: Request,
        background: BackgroundTasks,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        partial: Annotated[int, Query(ge=0, le=3)] = 0
) -> JSONResponse:
    """
    Retrieve academic load information for a student for a specific partial or period.

    Args:
        request (Request): The HTTP request object, automatically passed by FastAPI.
        background (BackgroundTasks): The background tasks object, used to run tasks asynchronously.
        enrollment (Annotated[str]): The student's enrollment ID. Must be exactly 15 characters.
        partial (Annotated[int]): The academic period to fetch data for (0 to 3, default is 0).

    Returns:
        JSONResponse: A response containing the student's academic load for the requested partial.
                      - On success: Status code 200 with the academic load data.
                      - On failure: Status code and error details.

    Authentication:
        Requires a valid bearer token in the `Authorization` header.
        The `authenticate` decorator ensures that the user is properly authenticated.

    Background Task:
        After processing the academic load, a background task (`check_student`) is triggered
        to perform further checks or operations asynchronously.

    Example:
        Request:
        GET {enrollment}/loads/?partial=2

        Response on success:
        {...}

        Response on failure:
        {
            "status": "Http argument",
            "message": "Custom exception"
        }
    """
    response = load.get_academic_loads(enrollment, partial).to_repr()
    background.add_task(check_student, response)

    return JSONResponse(
        status_code=200,
        content=response
    )


@load_routes.get("/semiannual", dependencies=[Depends(bearer)])
@authenticate
async def get_semiannual_academic_loads(
        request: Request,
        background: BackgroundTasks,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
) -> JSONResponse:
    """
        Retrieve semiannual academic load information for a student.

        Args:
            request (Request): The HTTP request object, automatically passed by FastAPI.
            background (BackgroundTasks): The background tasks object, used to run tasks asynchronously.
            enrollment (Annotated[str]): The student's enrollment ID. Must be exactly 15 characters.

        Returns:
            JSONResponse: A response containing the student's semiannual academic load.
                          - On success: Status code 200 with the semiannual academic load data.
                          - On failure: Status code and error details.

        Authentication:
            Requires a valid bearer token in the `Authorization` header.
            The `authenticate` decorator ensures that the user is properly authenticated.

        Background Task:
            After processing the semiannual academic load, a background task (`check_student`) is triggered
            to perform further checks or operations asynchronously.

        Example:
            Request:
            GET {enrollment}/loads/semiannual

            Response on success:
            {...}

            Response on failure:
            {
                "status": "Http argument",
                "message": "Custom exception"
            }
        """
    response = load.get_academic_loads(enrollment, 6).to_repr()
    background.add_task(check_student, response)

    return JSONResponse(
        status_code=200,
        content=response
    )
