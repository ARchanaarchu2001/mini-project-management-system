from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def create_user(self, payload: UserCreate) -> User:
        if self.user_repository.get_by_email(payload.email):
            raise BadRequestException("Email is already registered")

        user = User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role=payload.role,
        )
        self.user_repository.create(user)
        self.db.commit()
        return user

    def list_users(self) -> list[User]:
        return self.user_repository.get_all()
