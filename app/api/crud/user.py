from typing import Optional

from sqlalchemy.orm import Session

from app.api.crud.base import CRUD
from app.api.models import User
from app.api.v1.schemas.user import UserCreate, UserUpdate


class CRUDuser(CRUD[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, *, obj_in: UserCreate) -> User:
        # TODO
        pass
