from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Enum
import enum

PRECISION = 4
ASDECIMAL = False
SCALE = 1

class GoalsTasksStatusEnum(enum.Enum):
  Todo = "未着手"
  InProgress = "作業中"
  Completed = "完了"

class GoalsStatusEnum(enum.Enum):
  Unachieved = "未達成"
  Achieved = "達成"


class Goals(Base):
  __tablename__ = "goals"

  goal_id = Column(Integer,primary_key=True)
  goal_name = Column(String(50))
  status = Column(Enum(GoalsStatusEnum),nullable=False)
  start_day = Column(Date)
  completion_date = Column(Date)
  status_against_goal = Column(String(200))
  weekday_available_hours = Column(Float(PRECISION, ASDECIMAL, SCALE))
  weekends_available_hours = Column(Float(PRECISION, ASDECIMAL, SCALE))
  total_estimated_time = Column(Float(PRECISION, ASDECIMAL, SCALE))
  task_creation_rule = Column(String(800))
  created_at = Column(DateTime)

class GoalsTasks(Base):
  __tablename__ = "goals_tasks"

  goal_task_id = Column(Integer, ForeignKey("goals.goal_id"),primary_key=True)
  goal_task_name = Column(String(50))
  goal_task_status = Column(Enum(GoalsTasksStatusEnum), nullable=False)
  deadline = Column(Date)
  estimated_time = Column(Float(PRECISION, ASDECIMAL, SCALE))
  created_at = Column(DateTime)