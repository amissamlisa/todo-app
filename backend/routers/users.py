from starlette import status
from fastapi import APIRouter
from typing import Annotated
from ..schemas.schemas import UserPointsUpdateRequest, UserRankUpdateRequest
from ..database import get_db
from fastapi.params import Depends
from sqlalchemy.orm import Session
from backend.utils.auth_helpers import get_current_user
from backend.repository.repository import UserRepository
from fastapi import HTTPException

user_repository = UserRepository()
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
router = APIRouter(prefix="/users", tags=["users"])


@router.put("/points", status_code=status.HTTP_204_NO_CONTENT)
def update_points(
    user: user_dependency, db: db_dependency, payload: UserPointsUpdateRequest
):
    try:
        user_record = user_repository.update_user_points_from_db(
            db, user.get("user_id"), payload.points
        )
        if user_record is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.put("/rank", status_code=status.HTTP_204_NO_CONTENT)
def update_rank(
    user: user_dependency, db: db_dependency, payload: UserRankUpdateRequest
):
    try:
        user_record = user_repository.update_user_rank_from_db(
            db, user.get("user_id"), payload.user_rank
        )
        if user_record is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")
