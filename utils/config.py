"""
This module defines the `Config` class for managing application configuration settings.

The class reads environment variables from a `.env` file using the `dotenv` library and
provides them as class attributes. These configurations are used for handling security
and token-related settings.

Key Features:
- Automatically loads environment variables from a `.env` file.
- Provides centralized access to critical security configurations.

Dependencies:
- `dotenv` library for loading environment variables.
- `os` module for accessing environment variables.
"""
from os import getenv
from dotenv import load_dotenv


class Config:
    """
    Configuration class that loads and stores application settings from
    environment variables.

    Attributes:
        SECRET_KEY (str): Secret key used for signing or encrypting tokens.
        ACCESS_TOKEN (str): Default access token key for authentication.
        ALGORITHM (str): Algorithm used for token generation (e.g., "HS256", "HS512").
        TOKEN_EXPIRE_DAYS (int): Number of days until the token expires.
    """
    load_dotenv()

    SECRET_KEY = getenv("SECRET_KEY")
    ACCESS_TOKEN = getenv("ACCESS_TOKEN")
    ALGORITHM = getenv("ALGORITHM")
    TOKEN_EXPIRE_DAYS = int(getenv("TOKEN_EXPIRE_DAYS"))
