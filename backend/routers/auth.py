from fastapi import APIRouter
from ..models.models import Users
from ..schemas.schemas import UserRequest
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/auth")
def create_user(userRequest: UserRequest):
  user = Users(
    user_name=userRequest.user_name,
    email=userRequest.email,
    hashed_password=userRequest.bcrypt_context.hash(userRequest.password)
  )