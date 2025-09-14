from sqlalchemy.orm import Session
from ..models import Goals, GoalsTasks
from typing import List 

class GoalTaskRepository:
   def registerGoalAndGoalTasks(self, db: Session, goal: Goals, goal_tasks_list: List):
      db.add(goal)
      db.flush()
      db.refresh(goal)

      for task in goal_tasks_list:
         db.add(GoalsTasks(task))
         db.flush()
         db.refresh(goal)