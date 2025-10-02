from sqlalchemy.orm import Session
from ..models.models import Goals, GoalsTasks, DailyTasks
from typing import List
from fastapi import HTTPException

class GoalTaskRepository:
   def registerGoalAndGoalTasks(self, db: Session, goal: Goals, goal_task: GoalsTasks):
      try:
         db.add(goal)
         db.flush()
         db.refresh(goal)

         db.add(goal_task)
         db.flush()
         db.refresh(goal_task)
         db.commit()
      except Exception as e:
         raise e

class DailyTaskRepository:
   def registerDailyTask(self, db: Session, daily_task: DailyTasks):
      try:
         db.add(daily_task)
         db.flush()
         db.refresh(daily_task)

      except Exception as e:
         raise e
