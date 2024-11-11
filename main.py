from routes.student_routes import student_routes
from routes.auth_routes import auth_routes
from routes.load_routes import load_routes
from errors.errors import ServerBaseException, DatabaseError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, File, UploadFile
from typing import Annotated


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


@app.post("/load-database")
async def load_dbf(dbf_data: Annotated[UploadFile, File(...)]) -> JSONResponse:
    data = await dbf_data.read()

    try:
        with open(f"db/{dbf_data.filename}", "wb") as dbf:
            dbf.write(data)

        return JSONResponse(
            status_code=202,
            content={"status": f"Loaded database {dbf_data.filename} ✅"}
        )

    except Exception as e:
        raise DatabaseError() from e

student_routes.include_router(load_routes, prefix="/{enrollment}/loads")
app.include_router(student_routes, prefix="/students", tags=["Student"])
app.include_router(auth_routes, prefix="/auth", tags=["Auth"])
