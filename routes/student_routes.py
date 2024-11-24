from services.student_services import StudentServices
from decorators.authenticator import authenticate
from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
from utils.token import CustomHTTPBearer
from fastapi.requests import Request
from typing import Annotated

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
