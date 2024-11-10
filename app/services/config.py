import os

from fastapi.security import OAuth2PasswordBearer


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

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


config = Config
