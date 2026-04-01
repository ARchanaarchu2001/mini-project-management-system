from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_all(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.id.desc())).all())

    def count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(User)) or 0
