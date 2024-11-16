from services.history_services import HistoryServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Path, Query
from typing import Annotated

history_routes = APIRouter()
history = HistoryServices()


@history_routes.get("/")
async def get_history(
        enrollment: Annotated[str, Path(max_length=15, min_length=15)],
        rank: Annotated[int, Query(ge=1, le=6)]
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=history.get_history(enrollment, rank).to_repr()
    )
