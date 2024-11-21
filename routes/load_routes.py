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
    response = load.get_academic_loads(enrollment, 6).to_repr()
    background.add_task(check_student, response)

    return JSONResponse(
        status_code=200,
        content=response
    )
