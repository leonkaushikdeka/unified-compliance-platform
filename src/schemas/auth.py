from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from src.models.user import User
from src.models.assessment import Assessment, Framework


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str
    email: str
    tenant_id: str
    role: str
    exp: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_slug: Optional[str] = None


class LoginResponse(BaseModel):
    user: "UserResponse"
    tokens: Token
    requires_mfa: bool = False


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    tenant_name: str
    tenant_slug: str = Field(min_length=3, max_length=50, pattern=r"^[a-z0-9-]+$")


class RegisterResponse(BaseModel):
    user: "UserResponse"
    tokens: Token


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    is_active: bool
    email_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj: User) -> "UserResponse":
        return cls(
            id=obj.id,
            email=obj.email,
            first_name=obj.first_name,
            last_name=obj.last_name,
            role=obj.role,
            is_active=obj.is_active,
            email_verified=obj.email_verified,
            created_at=obj.created_at,
        )


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


UserResponse.model_rebuild()
