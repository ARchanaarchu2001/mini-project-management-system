from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.utils.dependencies import get_admin_user, get_current_user

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_admin_user),
) -> UserResponse:
    return UserService(db).create_user(payload)


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> list[UserResponse]:
    return UserService(db).list_users()
