from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime

class Goals(Base):
  __tablename__ = "goals"

  goal_id = Column(Integer,primary_key=True)
  goal_name = Column(String(50))
  status = Column(String(3))
  start_day = Column(Date)
  completion_date = Column(Date)
  status_against_goal = Column(String(200))
  weekday_available_hours = Column(Float(4, False, 1))
  weekends_available_hours = Column(Float(4, False, 1))
  total_estimated_time = Column(Float(4, False, 1))
  task_creation_rule = Column(String(800))
  created_at = Column(DateTime)

class GoalsTasks(Base):
  __tablename__ = "goals_tasks"

  goal_task_id = Column(Integer, ForeignKey("goals.goal_id"),primary_key=True)
  goal_task_name = Column(String(50))
  goal_task_status = Column(String(3))
  deadline = Column(Date)
  estimated_time = Column(Float(3, False, 1))
  created_at = Column(DateTime)