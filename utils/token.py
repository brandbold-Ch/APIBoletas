from datetime import datetime, timedelta
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from errors.errors import NotFoundTokenError, ExpiredTokenError, InvalidTokenError
from jose import jwt, JWTError


class CustomHTTPBearer(HTTPBearer):

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        self.auto_error = False
        credentials = await super().__call__(request)

        if credentials is None:
            raise NotFoundTokenError()

        request.state.token = credentials.credentials
        return credentials


def create_token(payload) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        "fArS619|QKL$",
        algorithm="HS256"
    )


def verify_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, "fArS619|QKL$",
            algorithms=["HS256"]
        )
        return decoded_token
    except JWTError as e:
        if str(e) == "Signature has expired.":
            raise ExpiredTokenError("Token has expired 💨") from e
        else:
            raise InvalidTokenError() from e
