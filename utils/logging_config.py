"""
This module configures logging for the application, specifically setting up a logger
to capture and store logs related to server operations and exceptions. The logs are stored
in a rotating log file, ensuring that the file size does not grow beyond a set limit.

Dependencies:
- logging: Standard library for logging functionality.
- logging.handlers.RotatingFileHandler: A handler that writes logs to a file with rotation.
"""

import logging
from logging.handlers import RotatingFileHandler

log_format = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)

log_handler_app = RotatingFileHandler('server_exceptions.log',
                                      maxBytes=10 ** 6, backupCount=5, encoding="utf-8")
log_handler_app.setFormatter(formatter)

app_logger = logging.getLogger('server')
app_logger.setLevel(logging.INFO)
app_logger.addHandler(log_handler_app)
