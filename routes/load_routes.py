from services.load_services import LoadServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path, Query
from typing import Annotated

load_routes = APIRouter()
load = LoadServices()


@load_routes.get("/")
async def get_score(
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        partial: Annotated[int, Query(ge=0, le=3)] = 0
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=load.get_loads(enrollment, partial).to_repr()
    )
