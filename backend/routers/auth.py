from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, timezone
from ..models.models import Users
from ..repository.repository import UserRepository
from ..schemas.schemas import UserRequest, Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'name': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='ユーザーを検証できません')

    except JWTError:
        raise HTTPException(status_code=401, detail='ユーザーを検証できません')

    return {'username': username, 'user_id': user_id}


@router.post("/")
def create_user(userRequest: UserRequest):
    db = next(get_db())
    user_repository = UserRepository()
    user = Users(
        username=userRequest.username,
        email=userRequest.email,
        hashed_password=bcrypt_context.hash(userRequest.password)
    )
    user_repository.register_user(db, user, commit=True)
    return {"statusCode": 201, "message": "新規ユーザー登録に成功"}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail='ユーザーを検証できません')
    token = create_access_token(user.username, user.user_id, timedelta(minutes=15))
    return {'access_token': token, 'token_type': 'bearer'}
