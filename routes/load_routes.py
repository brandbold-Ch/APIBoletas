from fastapi import APIRouter, Path, Query, Depends
from decorators.authenticator import authenticate
from services.load_services import LoadServices
from fastapi.responses import JSONResponse
from utils.token import CustomHTTPBearer
from fastapi.requests import Request
from typing import Annotated

load_routes = APIRouter()
load = LoadServices()
bearer = CustomHTTPBearer()


@load_routes.get("/", dependencies=[Depends(bearer)])
@authenticate
async def get_loads(
        request: Request,
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        partial: Annotated[int, Query(ge=0, le=3)] = 0
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=load.get_loads(enrollment, partial).to_repr()
    )
