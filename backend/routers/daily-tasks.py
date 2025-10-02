from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import DailyTasksRequest
from ..models.models import DailyTasks
from ..repository.tasks_repository import DailyTaskRepository

router = APIRouter(
    prefix="/todos",
    tags=["daily-tasks"]
)

@router.post("/daily-tasks-registration", status_code=status.HTTP_201_CREATED)
def save_goal_tasks(dailyTaskRequest: DailyTasksRequest, db: Session = Depends(get_db)):
    daily_task_repository = DailyTaskRepository()
    daily_task = DailyTasks(**dailyTaskRequest.model_dump())
    try:
        daily_task_repository.registerDailyTask(db, daily_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("日常タスクの登録に失敗しました"))
    return {"status":"ok", "message": "日常タスクが保存されました"}