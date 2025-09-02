from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime

class GoalsTasksStatus(Enum):
  Todo = "未着手"
  InProgress = "作業中"
  Completed = "完了"

class GoalsTasksRequest(BaseModel):
  goal_name: str = Field(max_length=50)
  status_against_goal: str = Field(max_length=200)
  start_date: datetime.date
  completion_date: datetime.date
  weekday_available_hours: float
  weekends_available_hours: float
  task_creation_rule: Optional[str] = Field(max_length=800)

class GoalsTasksOut(BaseModel):
  goal_name: str = Field(max_length=50)
  deadline: datetime.date
  estimated_time: float
  status: GoalsTasksStatus = GoalsTasksStatus.Todo