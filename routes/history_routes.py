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
    return JSONResponse(
        status_code=200,
        content=history.get_histories(enrollment, rank, 6).to_repr()
    )
