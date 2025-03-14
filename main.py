"""
This FastAPI application provides RESTful endpoints for managing academic records
at COBACH Plantel 217 Soconusco. It includes features such as loading a database
from a DBF file and handling exceptions.

Features:
- Load database from a DBF file (POST `/load-database`).
- Handle student records with routes for loading and viewing histories (via `/students`).
- Provide authentication routes via `/auth`.

The application includes proper error handling and middleware for cross-origin requests.

Components:
- **CORS Middleware**: Allows cross-origin requests from any origin.
- **Custom Exception Handlers**: Handle `ServerBaseException`, `DatabaseError`, and `TokenNotAllowed`.
- **Environment Variables**: Loaded using `dotenv` to manage secrets and tokens.
"""
from typing import Annotated
from fastapi import FastAPI, Request, File, UploadFile, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.student_routes import student_routes
from routes.auth_routes import auth_routes
from routes.load_routes import load_routes
from routes.history_routes import history_routes
from errors.errors import ServerBaseException, ServerError, TokenNotAllowed
from tasks.fastapi_tasks import run_main, main
from utils.config_secrets import Config
from middlewares.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="COBACH Plantel 2️⃣1️⃣7️⃣ Soconusco. 🏫",
    description="API Rest para obtención de boletas académicas. 📃",
    version="1.0.0",
    root_path="/api"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)


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
        background: BackgroundTasks,
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
        :param access:
        :param dbf_data:
        :param background:
    """

    if access == Config.ACCESS_TOKEN:
        read_data = await dbf_data.read()
        file_name = dbf_data.filename.lower()

        with open(f"db/{file_name}", "wb") as dbf:
            dbf.write(read_data)

        if file_name == "cargas.dbf":
            await main()

        return JSONResponse(
            status_code=202,
            content={"status": f"Loaded database {file_name} ✅"}
        )

    raise TokenNotAllowed()


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
