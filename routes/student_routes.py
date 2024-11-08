from services.student_services import StudentServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path
from typing import Annotated

student_routes = APIRouter()
student = StudentServices()


@student_routes.get("/{enrollment}")
async def get_student(
        enrollment: Annotated[str, Path(max_length=15, min_length=15)]
) -> JSONResponse:
    return JSONResponse(status_code=200, content=student.get_student(enrollment).to_repr())
