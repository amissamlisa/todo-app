from typing import Annotated

from backend.repository.repository import (
    GoalRepository,
    GoalTaskRepository,
    UserRepository,
)
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.utils.auth_helpers import get_current_user
from ..database import get_db
from ..schemas.schemas import UserPointsUpdateRequest, UserRankUpdateRequest

router = APIRouter(prefix="/top", tags=["top"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

user_repository = UserRepository()
goal_repository = GoalRepository()
goal_task_repository = GoalTaskRepository()


@router.put("/points", status_code=status.HTTP_201_CREATED)
def update_points(
    user: user_dependency, db: db_dependency, payload: UserPointsUpdateRequest
):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="認証に失敗しました")

        user_record = user_repository.update_user_points_from_db(
            db, user.get("user_id"), payload.points
        )
        if user_record is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")

@router.put("/rank", status_code=status.HTTP_201_CREATED)
def update_rank(
    user: user_dependency, db: db_dependency, payload: UserRankUpdateRequest
):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="認証に失敗しました")

        user_record = user_repository.update_user_rank_from_db(
            db, user.get("user_id"), payload.user_rank
        )
        if user_record is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.get("", status_code=status.HTTP_200_OK)
def read_top_screen_info(user: user_dependency, db: db_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="認証に失敗しました")

        user_record = user_repository.find_user_by_user_id(db, user.get("user_id"))
        if user_record is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        goals = goal_repository.find_goal_by_user_id(db, user_record.user_id)
        goal = goals[0] if goals else None
        goal_tasks = (
            goal_task_repository.find_goal_task_by_goal_id(db, goal.goal_id)
            if goal
            else []
        )

        goal_data = (
            {
                "goal_id": goal.goal_id,
                "user_id": goal.user_id,
                "goal_name": goal.goal_name,
                "status": goal.status,
                "start_day": goal.start_day.isoformat(),
                "target_day": goal.target_day.isoformat(),
                "status_against_goal": goal.status_against_goal,
                "weekday_available_time": goal.weekday_available_time,
                "weekends_available_time": goal.weekends_available_time,
                "total_estimated_time": goal.total_estimated_time,
                "task_creation_rule": goal.task_creation_rule,
            }
            if goal
            else None
        )

        goal_tasks_data = [
            {
                "goal_task_id": goal_task.goal_task_id,
                "goal_id": goal_task.goal_id,
                "order_num": goal_task.order_num,
                "goal_task_name": goal_task.goal_task_name,
                "goal_task_status": goal_task.goal_task_status,
                "deadline": goal_task.deadline.isoformat(),
                "estimated_time": goal_task.estimated_time,
            }
            for goal_task in goal_tasks
        ]

        return {
            "username": user_record.username,
            "email": user_record.email,
            "user_rank": user_record.user_rank,
            "user_points": user_record.user_points,
            "goal": goal_data,
            "goal_tasks": goal_tasks_data,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")
