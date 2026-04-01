from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, payload: UserRegister) -> User:
        if self.user_repository.get_by_email(payload.email):
            raise BadRequestException("Email is already registered")

        role = (
            UserRole.ADMIN
            if self.user_repository.count() == 0
            else UserRole.DEVELOPER
        )

        user = User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role=role,
        )
        self.user_repository.create(user)
        self.db.commit()
        return user

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password):
            raise BadRequestException("Invalid email or password")
        return TokenResponse(access_token=create_access_token(str(user.id)))
