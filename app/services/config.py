import os

from decouple import config
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}".format(
            DB_USER=os.getenv("POSTGRES_USER", "postgres"),
            DB_PASSWORD=os.getenv("POSTGRES_PASSWORD", "your_password"),
            DB_URL=os.getenv("DB_URL", "localhost"),
            DB_PORT=os.getenv("DB_PORT", "5432"),
            DB_NAME=os.getenv("POSTGRES_DB", "your_db_name"),
        ),
    )

    JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="your_default_secret_key")


# JWT Settings
class Settings(BaseModel):
    authjwt_secret_key: str = Config.JWT_SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
