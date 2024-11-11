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
    return JSONResponse(status_code=200, content=student.get_student(enrollment).to_repr())
