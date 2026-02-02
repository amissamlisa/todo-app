from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import JWTError, jwt

from .generate_secure_string import generate_secure_string
from ..models.models import PasswordResetTokens, RefreshTokens
from ..repository.repository import (
    UserRepository,
    RefreshTokenRepository,
    PasswordResetRepository,
)
from ..database import get_db
from ..config import settings
from ..exceptions.app_exception import AppException
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = AppException(
    status_code=401,
    error_code="NOT_AUTHENTICATED",
    error_message="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

token_generation_exception = AppException(
    error_code="TOKEN_GENERATION_FAILED",
    error_message="failed to generate unique token",
    status_code=500,
)

invalid_password_reset_link_exception = AppException(
    error_code="INVALID_LINK_ERROR",
    error_message="the password reset link is invalid",
    status_code=404,
)

expired_password_reset_link_exception = AppException(
    error_code="EXPIRED_LINK_ERROR",
    error_message="the password reset link is expired",
    status_code=404,
)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return {"username": username, "user_id": user_id}


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user_repository = UserRepository()
    user = user_repository.find_user_by_email(db, email)
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_token(user_id: int, expires_delta: timedelta):
    encode = {"sub": str(user_id)}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int, db: Session):
    refresh_token_repository = RefreshTokenRepository()
    for _ in range(3):
        raw_token = generate_secure_string(length=60)
        hashed_token = bcrypt_context.hash(raw_token)
        token_prefix = raw_token[:6]
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        try:
            refresh_token_record = RefreshTokens(
                user_id=user_id,
                token_prefix=token_prefix,
                hashed_token=hashed_token,
                expires_at=datetime.now(timezone.utc) + refresh_token_expires,
            )
            refresh_token_repository.register_refresh_token(
                db, refresh_token_record, commit=True
            )
            return raw_token

        except IntegrityError:
            logger.error("失敗しました。もう一度繰り返します")

    raise token_generation_exception


def create_password_reset_token(user_id: int, db: Session = Depends(get_db)):
    password_reset_token_repository = PasswordResetRepository()

    for _ in range(3):
        raw_token = generate_secure_string(length=60)
        hashed_token = bcrypt_context.hash(raw_token)
        token_prefix = raw_token[:6]
        password_reset_token_expires = datetime.now(timezone.utc) + timedelta(
            hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS
        )

        try:
            password_reset_token_record = PasswordResetTokens(
                user_id=user_id,
                token_prefix=token_prefix,
                hashed_token=hashed_token,
                expires_at=password_reset_token_expires,
            )
            password_reset_token_repository.register_password_reset_token(
                db, password_reset_token_record
            )
            return raw_token

        except IntegrityError:
            logger.error("失敗しました。もう一度繰り返します")
    raise token_generation_exception


def find_valid_password_token(password_reset_token: str, db: Session):

    password_reset_repository = PasswordResetRepository()
    matched_token = None
    if not password_reset_token:
        raise invalid_password_reset_link_exception
    password_reset_token_prefix = password_reset_token[:6]
    password_reset_token_records = (
        password_reset_repository.get_password_refresh_token_by_prefix(
            db, password_reset_token_prefix
        )
    )

    if not password_reset_token_records:
        raise invalid_password_reset_link_exception
    for token_record in password_reset_token_records:
        if bcrypt_context.verify(password_reset_token, token_record.hashed_token):
            matched_token = token_record
            if not matched_token:
                raise invalid_password_reset_link_exception
            elif matched_token.expires_at < datetime.now(timezone.utc):
                raise expired_password_reset_link_exception
            return matched_token
    raise invalid_password_reset_link_exception


def get_token_from_cookie(refresh_token: str | None = Cookie(default=None)):
    if refresh_token is None:
        raise credentials_exception
    return refresh_token


def verify_and_find_refresh_token(refresh_token: str, db: Session):
    token_prefix = refresh_token[:6]
    token_records = (
        db.query(RefreshTokens).filter(RefreshTokens.token_prefix == token_prefix).all()
    )
    for record in token_records:
        if bcrypt_context.verify(refresh_token, record.hashed_token):
            return record
    return None
