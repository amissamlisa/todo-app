from sqlalchemy.orm import Session
from ..models.models import Goals, GoalsTasks, DailyTasks, Users

class GoalTaskRepository:
   def __init__(self):
      pass  

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
   def __init__(self):
      pass
   def registerDailyTask(self, db: Session, daily_task: DailyTasks):
      try:
         db.add(daily_task)
         db.flush()
         db.refresh(daily_task)
         db.commit()

      except Exception as e:
         raise e

class UserRepository:
   def __init__(self):
      pass
   def registerUser(self, db: Session, user: Users):
      try:
         db.add(user)
         db.flush()
         db.refresh(user)
         db.commit()

      except Exception as e:
         raise e
