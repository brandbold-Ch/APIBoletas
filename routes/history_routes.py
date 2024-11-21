from services.history_services import HistoryServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path, Query
from typing import Annotated

history_routes = APIRouter()
history = HistoryServices()


@history_routes.get("/")
async def get_history(
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        rank: Annotated[int, Query(ge=1, le=6)],
        partial: Annotated[int, Query(ge=1, le=3)],
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=history.get_histories(enrollment, rank, partial).to_repr()
    )
