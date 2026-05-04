from fastapi import APIRouter, Depends, HTTPException, status, Response
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated


from backend.exceptions.app_exception import AppException
from backend.utils.email_helpers import send_email
from backend.utils.auth_helpers import (
    authenticate_user,
    create_token,
    create_refresh_token,
    create_password_reset_token,
    find_valid_password_token,
    get_token_from_cookie,
    hash_password,
    credentials_exception,
    invalid_password_reset_link_exception,
    verify_and_find_refresh_token,
)
from backend.utils.validation_helpers import validate_password_byte_length
from ..models.models import Users
from ..repository.repository import (
    EmailAlreadyRegistered,
    PasswordResetRepository,
    UserRepository,
    RefreshTokenRepository,
)
from ..schemas.schemas import (
    PasswordResetEmailRequest,
    PasswordResetRequest,
    UserRequest,
    Token,
)
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

password_reset_repository = PasswordResetRepository()
refresh_token_repository = RefreshTokenRepository()
user_repository = UserRepository()


@router.post("/password-reset/request", status_code=status.HTTP_201_CREATED)
def send_reset_password_email(
    password_reset_email_request: PasswordResetEmailRequest,
    db: Session = Depends(get_db),
):
    user_email = password_reset_email_request.email
    user = user_repository.find_user_by_email(db, user_email)

    if not user:
        raise HTTPException(
            status_code=404, detail="送信されたメールアドレスは無効です"
        )
    password_reset_token = create_password_reset_token(user.user_id, db)

    message = f"""{user.username}さん

パスワード再設定のリンクを受け付けました。
下記のリンクからパスワードをリセットしてください。

{settings.PASSWORD_RESET_URL}?token={password_reset_token}

パスワード再設定リンクの有効期限は1時間です。
1時間以内にパスワード変更を実施してください。
"""
    from_addr = settings.SENDER_ADDRESS
    to_addr = user_email
    subject = "[Claidy Todo] パスワード再設定のご案内"

    send_email(
        from_addr,
        to_addr,
        message,
        subject,
        settings.SENDER_ADDRESS,
        settings.SENDER_ADDRESS_PASSWORD,
    )
    return {"message": "A password reset link has been sent"}


@router.get("/password-reset/verification", status_code=status.HTTP_200_OK)
def verify_password_reset_link(token: str, db: Session = Depends(get_db)):
    password_reset_token_record = find_valid_password_token(
        token,
        db,
    )

    if not password_reset_token_record:
        raise invalid_password_reset_link_exception
    return {"message": "Valid password reset link"}


@router.put("/password-reset", status_code=status.HTTP_201_CREATED)
def reset_password(
    password_reset_request: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    record = find_valid_password_token(password_reset_request.token, db)
    hashed_new_password = hash_password(password_reset_request.password)

    password_reset_repository.update_password_from_db(
        db, record.user_id, hashed_new_password, commit=True
    )
    refresh_token_repository.revoke_all_user_tokens(db, record.user_id, commit=True)

    return {"message": "Password has been reset successfully"}


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserRequest, db: Session = Depends(get_db)):
    user = Users(
        username=user_request.username,
        email=user_request.email,
        hashed_password=hash_password(user_request.password),
    )
    try:
        user_repository.register_user(db, user, commit=True)
    except EmailAlreadyRegistered:
        raise AppException(
            status_code=400,
            error_code="EMAIL_ALREADY_REGISTERED",
            error_message="This email is already registered",
        )
    return {"message": "The user has been registered successfully"}


@router.delete("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Depends(get_token_from_cookie),
):
    matched_refresh_token = verify_and_find_refresh_token(refresh_token, db)

    if matched_refresh_token:
        refresh_token_repository.revoke_refresh_token(
            db, matched_refresh_token.refresh_token_id
        )

    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "Logged out successfully"}


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    try:
        validate_password_byte_length(form_data.password)
    except ValueError as exc:
        raise AppException(
            status_code=422,
            error_code="PASSWORD_TOO_LONG",
            error_message=str(exc),
        )
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise AppException(
            status_code=401,
            error_code="INVALID_PASSWORD_OR_EMAIL",
            error_message="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        user.user_id, user.username, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(user.user_id, db)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str = Depends(get_token_from_cookie),
):
    if not refresh_token:
        raise AppException(
            status_code=401,
            error_code="REFRESH_TOKEN_MISSING",
            error_message="Refresh token is missing or invalid.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    matched_refresh_token = verify_and_find_refresh_token(refresh_token, db)
    if not matched_refresh_token or matched_refresh_token.expires_at < datetime.now(
        timezone.utc
    ):
        raise credentials_exception

    if matched_refresh_token.revoked_at is not None:
        refresh_token_repository.revoke_all_user_tokens(
            db, matched_refresh_token.user_id, commit=True
        )
        raise AppException(
            status_code=401,
            error_code="REFRESH_TOKEN_REUSE_DETECTED",
            error_message="Refresh token reuse detected. All sessions have been invalidated for security.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = matched_refresh_token.user_id
    user = user_repository.find_user_by_user_id(db, user_id)
    if user is None:
        raise credentials_exception
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        user_id, user.username, expires_delta=access_token_expires
    )

    refresh_token_repository.revoke_refresh_token(
        db, matched_refresh_token.refresh_token_id, commit=True
    )

    new_refresh_token = create_refresh_token(user_id, db)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path="/",
    )

    return {"access_token": access_token, "token_type": "bearer"}
