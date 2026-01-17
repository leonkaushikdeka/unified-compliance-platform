from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_db
from src.core.logging import get_logger
from src.models.user import Tenant, User
from src.models.audit import AuditLog
from src.services.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    create_refresh_token_record,
    create_user,
    decode_token,
    revoke_refresh_token,
    validate_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
)
from src.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    RefreshTokenRequest,
    Token,
    UserResponse,
    PasswordChangeRequest,
)

logger = get_logger(__name__)
router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, login_data.email, login_data.password)
    if not user:
        logger.warning("Failed login attempt", email=login_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role,
        }
    )
    refresh_token = create_refresh_token(data={"sub": user.id})
    expires_at = datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    await create_refresh_token_record(
        db=db,
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    user.last_login = datetime.utcnow()
    await db.flush()

    await db.execute(
        AuditLog.__table__.insert().values(
            AuditLog.create_entry(
                tenant_id=user.tenant_id,
                user_id=user.id,
                action="user.login",
                details={"email": user.email},
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
            ).__dict__
        )
    )
    await db.commit()

    return LoginResponse(
        user=UserResponse.from_orm(user),
        tokens=Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
        ),
    )


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    existing_user = await db.execute(select(User).where(User.email == register_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    tenant = Tenant(
        id=str(uuid4()),
        name=register_data.tenant_name,
        slug=register_data.tenant_slug,
        plan="starter",
    )
    db.add(tenant)
    await db.flush()

    user = await create_user(
        db=db,
        email=register_data.email,
        password=register_data.password,
        tenant_id=tenant.id,
        first_name=register_data.first_name,
        last_name=register_data.last_name,
        role="admin",
    )

    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role,
        }
    )
    refresh_token = create_refresh_token(data={"sub": user.id})
    expires_at = datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    await create_refresh_token_record(
        db=db,
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    await db.commit()

    return RegisterResponse(
        user=UserResponse.from_orm(user),
        tokens=Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token,
        ),
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    stored_token = await validate_refresh_token(db, refresh_data.refresh_token)
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    payload = decode_token(refresh_data.refresh_token)
    if not payload or payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user = await db.execute(select(User).where(User.id == payload.sub, User.is_active == True))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    await revoke_refresh_token(db, refresh_data.refresh_token)

    new_access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "role": user.role,
        }
    )
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    expires_at = datetime.utcnow() + datetime.timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    await create_refresh_token_record(
        db=db,
        user_id=user.id,
        token=new_refresh_token,
        expires_at=expires_at,
    )

    await db.commit()

    return Token(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=new_refresh_token,
    )


@router.post("/logout")
async def logout(
    refresh_data: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await revoke_refresh_token(db, refresh_data.refresh_token)
    await db.commit()

    await db.execute(
        AuditLog.__table__.insert().values(
            AuditLog.create_entry(
                tenant_id=current_user.tenant_id,
                user_id=current_user.id,
                action="user.logout",
            ).__dict__
        )
    )
    await db.commit()

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.from_orm(current_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    current_user.password_hash = hash_password(password_data.new_password)
    await db.commit()

    await db.execute(
        AuditLog.__table__.insert().values(
            AuditLog.create_entry(
                tenant_id=current_user.tenant_id,
                user_id=current_user.id,
                action="user.password_changed",
            ).__dict__
        )
    )
    await db.commit()

    return {"message": "Password changed successfully"}
