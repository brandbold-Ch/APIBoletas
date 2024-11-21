from services.auth_services import AuthServices
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body
from typing import Annotated

auth_routes = APIRouter()
auth = AuthServices()


@auth_routes.post("/login")
async def login(
        username: Annotated[str, Body(max_length=18, min_length=18)],
        password: Annotated[str, Body(max_length=15, min_length=15)]
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=auth.login(username, password)
    )

