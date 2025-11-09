from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models.models import Goals, GoalsStatusEnum, GoalsTasks
from .auth import get_current_user
from ..repository.repository import GoalRepository, StatusUnchangedError, GoalNotFound, GoalTaskRepository

router = APIRouter(
    prefix="/goal",
    tags=["goal"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/{goal_id}", status_code=status.HTTP_200_OK)
def read_goal(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")
        goal = db.query(Goals).filter(Goals.status == GoalsStatusEnum.Unachieved.value,
                                      Goals.goal_id == goal_id).first()

        if goal is None:
            raise HTTPException(status_code=404, detail='目標が見つかりません')

        return {"detail": "目標を取得しました", "goal": goal}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_and_goal_tasks(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        goal_repository = GoalRepository()
        goal_tasks_repository = GoalTaskRepository()
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")
        goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
        if goal is None:
            raise HTTPException(status_code=404, detail='目標が見つかりません')
        goal_tasks = db.query(GoalsTasks).filter(GoalsTasks.goal_id == goal_id).all()
        if goal_tasks is None:
            raise HTTPException(status_code=404, detail='目標達成タスクが見つかりません')

        for goal_task in goal_tasks:
            goal_tasks_repository.delete_goal_task_from_db(db, goal_task, commit=True)
        goal_repository.delete_goal_from_db(db, goal, commit=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが削除できません")


@router.put("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_status(user: user_dependency, db: db_dependency, goal_id: int, new_status: GoalsStatusEnum):
    try:
        goal_repository = GoalRepository()
        if user is None:
            raise HTTPException(status_code=404, detail="認証に失敗しました")

        updated_goal = goal_repository.update_goal_status_from_db(
            db, goal_id, new_status, commit=True
        )
        if updated_goal is None:
            raise HTTPException(status_code=404, detail="目標タスクが見つかりません")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StatusUnchangedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except GoalNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが登録されません")
