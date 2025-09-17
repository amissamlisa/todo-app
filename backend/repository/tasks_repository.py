from sqlalchemy.orm import Session
from ..models.models import Goals, GoalsTasks
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
