import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

load_dotenv()


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

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60


config = Config
