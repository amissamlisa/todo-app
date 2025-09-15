from sqlalchemy.orm import Session
from ..models import Goals, GoalsTasks
from typing import List
from fastapi import HTTPException

class GoalTaskRepository:
   def registerGoalAndGoalTasks(self, db: Session, goal: Goals, goal_tasks_list: List):
      try:
         db.add(goal)
         db.flush()
         db.refresh(goal)

         for task in goal_tasks_list:
            task_instance = GoalsTasks(**task)
            db.add(task_instance)
            db.flush()
            db.refresh(task_instance)
         return {"status":"ok", "message": "達成目標と目標達成タスクが保存されました"}
      except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
