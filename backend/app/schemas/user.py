from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr


class UserRegister(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserCreate(UserRegister):
    role: UserRole = UserRole.DEVELOPER


class UserResponse(UserBase):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
