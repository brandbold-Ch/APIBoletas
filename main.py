from routes.student_routes import student_routes
from routes.auth_routes import auth_routes
from routes.load_routes import load_routes
from routes.history_routes import history_routes
from errors.errors import ServerBaseException, DatabaseError, TokenNotAllowed
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated


app = FastAPI(
    title="COBACH Plantel 2️⃣1️⃣7️⃣ Soconusco. 🏫",
    description="API Rest para obtención de boletas académicas. 📃",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY2hvb2wiOiJDT0JBQ0ggUGxhbnRlbCAyMTciLCJ0eXBlIjoiUHJlcGFyYXRvcmlhIn0.wINe8sP5B4bhbXC9ciAPXewvyK4b4bESgnXafJIWVGQ"


@app.exception_handler(ServerBaseException)
async def server_base_exception_handler(request: Request, exc: ServerBaseException) -> JSONResponse:
    """
    Custom exception handler for `ServerBaseException`.

    This function catches the `ServerBaseException` and returns a JSON response
    with the exception's status code and message.

    Args:
        request (Request): The incoming HTTP request.
        exc (ServerBaseException): The exception raised during request processing.

    Returns:
        JSONResponse: A response containing the error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


@app.post("/load-database")
async def load_dbf(
        dbf_data: Annotated[UploadFile, File(...)],
        access: Annotated[str, Query(...)]
) -> JSONResponse:
    """
    Endpoint to load database from a DBF file.

    This endpoint requires a valid access token. If the token is correct,
    it saves the uploaded DBF file to the server's local storage. If any errors occur
    during file handling, a `DatabaseError` is raised.

    Args:
        dbf_data (UploadFile): The DBF file to be uploaded.
        access (str): Access token for authorization.

    Returns:
        JSONResponse: A response indicating the success or failure of the database load operation.
    """
    if access != token:
        raise TokenNotAllowed()
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


@app.get("/")
async def welcome_message() -> JSONResponse:
    """
    Welcome message for the root endpoint.

    This endpoint returns a message indicating the API's status and its purpose.

    Returns:
        JSONResponse: A response containing the API status and description.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "OK 🆗",
            "message": "API Rest para el COBACH Plantel 2️⃣1️⃣7️⃣. 🏫",
            "details": "Con fines para la obtención de boletas acádemicas",
            "codes": {
                "status_code": 200,
                "error_code": None
            }
        }
    )

student_routes.include_router(load_routes, prefix="/{enrollment}/loads")
student_routes.include_router(history_routes, prefix="/{enrollment}/histories")
app.include_router(student_routes, prefix="/students", tags=["Student"])
app.include_router(auth_routes, prefix="/auth", tags=["Auth"])
