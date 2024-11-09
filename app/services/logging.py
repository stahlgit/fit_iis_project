import datetime
import logging
import os
import sys
from functools import wraps
from pathlib import Path
from typing import (  # even though callable is now in python, import it from typing to avoid errors for users with older versions of python
    Callable,
)

from fastapi import HTTPException

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)  # create logs directory if not exists


logger = logging.getLogger(__name__)
log_filename = LOG_DIR / f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # LOG to file
        logging.StreamHandler(sys.stdout),  # LOG to console
    ],
)

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def log_endpoint(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        endpoint_name = func.__name__
        logger.info(f"Entering endpoint: {endpoint_name}")

        try:
            response = await func(*args, **kwargs)
            logger.info(f"Successfully exited endpoint: {endpoint_name}")
            return response
        except HTTPException as http_exc:
            logger.error(f"HTTPException in {endpoint_name}: {http_exc.detail}")
            raise http_exc
        except Exception as e:
            logger.error(f"Exception in {endpoint_name}: {e}")
            raise HTTPException(status_code=400, detail=f"Error occurred: {e}")

    return wrapper
