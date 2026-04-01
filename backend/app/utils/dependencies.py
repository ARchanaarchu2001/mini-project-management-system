from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise UnauthorizedException("Invalid or expired token")

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise UnauthorizedException("User not found")
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException("Admin access is required")
    return current_user
