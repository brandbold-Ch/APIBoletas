from sys import prefix

from routes.score_routes import report_routes
from routes.student_routes import student_routes
from routes.auth_routes import auth_routes
from errors.errors import ServerBaseException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request


app = FastAPI(
    title="COBACH Plantel 2️⃣1️⃣7️⃣ Soconusco. 🏫",
    description="API Rest para obtención de boletas académicas. 📃",
    version="1.0.0"
)


@app.exception_handler(ServerBaseException)
async def server_base_exception_handler(request: Request, exc: ServerBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

student_routes.include_router(report_routes, prefix="/{enrollment}/score")
app.include_router(student_routes, prefix="/students", tags=["Student"])
app.include_router(auth_routes, prefix="/auth", tags=["Auth"])
