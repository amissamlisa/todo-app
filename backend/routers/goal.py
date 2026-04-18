from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.exc import IntegrityError, StatementError, DataError
from backend.schemas.schemas import SaveRequest
from backend.utils.auth_helpers import get_current_user

from ..database import get_db
from ..models.models import Goals, GoalsStatusEnum, GoalsTasks

from ..repository.repository import (
    GoalRepository,
    StatusUnchangedError,
    GoalNotFound,
    GoalTaskRepository,
    UnachievedGoalAlreadyExists,
)

router = APIRouter(prefix="/goal", tags=["goal"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
goal_repository = GoalRepository()
goal_task_repository = GoalTaskRepository()


@router.post("/", status_code=status.HTTP_201_CREATED)
def save_goals_and_goal_tasks_and(
    user: user_dependency, payload: SaveRequest, db: Session = Depends(get_db)
):
    try:
        goal = payload.goal
        total_estimated_time = payload.goal_total_estimated_time
        goal_task_list = payload.goal_tasks
        goal_data = goal.model_dump(exclude={"status"})
        goal_data["status"] = GoalsStatusEnum.Unachieved.value

        goal_obj = Goals(**goal_data, user_id=user.get("user_id"))
        goal_obj.total_estimated_time = total_estimated_time
        goal_repository.register_goal(db, goal_obj, commit=True)
        goal_task_items = []
        for goal_task in goal_task_list:
            task_data = goal_task.model_dump(exclude_none=True)
            if "goal_task_status" in task_data:
                task_data["goal_task_status"] = task_data["goal_task_status"].value
            goal_task_items.append(GoalsTasks(**task_data, goal_id=goal_obj.goal_id))
        goal_task_repository.register_goal_task(db, goal_task_items, commit=True)
        return {
            "detail": "達成目標と目標達成タスクが保存されました",
            "goal_id": goal_obj.goal_id,
        }
    except HTTPException:
        db.rollback()
        raise
    except UnachievedGoalAlreadyExists as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except (ValueError, IntegrityError, StatementError, DataError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが登録されません")


@router.get("/{goal_id}", status_code=status.HTTP_200_OK)
def read_goal(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        goal = (
            db.query(Goals)
            .filter(
                Goals.status == GoalsStatusEnum.Unachieved.value,
                Goals.goal_id == goal_id,
            )
            .first()
        )

        if goal is None:
            raise HTTPException(status_code=404, detail="目標が見つかりません")

        return {"detail": "目標を取得しました", "goal": goal}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが取得できません")


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_and_goal_tasks(user: user_dependency, db: db_dependency, goal_id: int):
    try:
        goal = goal_repository.fetch_goal_by_id_from_db(db, goal_id)
        if goal is None:
            raise HTTPException(status_code=404, detail="目標が見つかりません")
        goal_tasks = goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            db, goal_id
        )

        for goal_task in goal_tasks:
            goal_task_repository.delete_goal_task_from_db(db, goal_task, commit=True)
        goal_repository.delete_goal_from_db(db, goal, commit=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが削除できません")


@router.patch("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_goal_status(
    user: user_dependency, db: db_dependency, goal_id: int, new_status: GoalsStatusEnum
):
    try:
        updated_goal = goal_repository.update_goal_status_from_db(
            db, goal_id, new_status, commit=True
        )
        if updated_goal is None:
            raise HTTPException(status_code=404, detail="目標が見つかりません")
    except HTTPException:
        raise
    except (ValueError, GoalNotFound, StatusUnchangedError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが更新できません")


@router.put("/", status_code=status.HTTP_201_CREATED)
def update_goals_and_goal_tasks(
    user: user_dependency, payload: SaveRequest, db: Session = Depends(get_db)
):
    try:
        goal = payload.goal
        total_estimated_time = payload.goal_total_estimated_time
        goal_task_list = payload.goal_tasks
        goal_data = goal.model_dump()

        goal_data["status"] = GoalsStatusEnum.Unachieved.value

        goal_obj = Goals(**goal_data, user_id=user.get("user_id"))
        goal_obj.total_estimated_time = total_estimated_time
        updated_goal = goal_repository.update_goal_from_db(db, goal_obj, commit=True)

        new_goal_task_items = []
        for goal_task in goal_task_list:
            task_data = goal_task.model_dump(exclude_none=True)
            if "goal_task_status" in task_data:
                task_data["goal_task_status"] = task_data["goal_task_status"].value
            new_goal_task_items.append(
                GoalsTasks(**task_data, goal_id=updated_goal.goal_id)
            )
        goal_task_repository.replace_goal_tasks_from_db(
            db, updated_goal.goal_id, new_goal_task_items, commit=True
        )
        return {
            "detail": "達成目標と目標達成タスクが更新されました",
            "goal_id": goal_obj.goal_id,
        }
    except HTTPException:
        db.rollback()
        raise
    except GoalNotFound as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except (ValueError, IntegrityError, StatementError, DataError) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"{str(e)}: データが登録されません")
