from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models.models import Goals, GoalsStatusEnum, GoalsTasks
from .auth import get_current_user
from ..repository.repository import GoalRepository

router = APIRouter(
    prefix="/goal",
    tags=["goal"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{goal_id}",status_code=status.HTTP_200_OK)
def read_goal(user: user_dependency, db: db_dependency, goal_id: int):
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")
    goal = db.query(Goals).filter(Goals.status == GoalsStatusEnum.Unachieved.value, Goals.goal_id == goal_id).first()

    if goal is not None:
        return goal

    raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(user: user_dependency, db: db_dependency, goal_id: int):
    goal_repository = GoalRepository()
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")
    goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()

    if goal is None:
        raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')

    goal_repository.delete_goal_from_db(db, goal, commit=True)


@router.put("/{goal_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_goal_status(user: user_dependency, db: db_dependency, goal_id: int, new_status: GoalsStatusEnum):
    goal_repository = GoalRepository()
    if user is None:
        raise HTTPException(status_code=404, detail="認証に失敗")

    updated_goal = goal_repository.update_goal_status_from_db(
        db, goal_id, new_status, commit=True
    )
    # print(updated_goal.goal_task_status)

    if updated_goal is None:
        raise HTTPException(status_code=404, detail="目標タスクが見つかりません")

    return {"message": "ステータスを更新しました"}