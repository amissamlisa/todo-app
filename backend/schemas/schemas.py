from pydantic import BaseModel, Field, model_validator
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
  target_date: datetime.date
  weekday_available_hours: float
  weekends_available_hours: float
  task_creation_rule: Optional[str] = Field(max_length=800)

  @model_validator(mode="after")
  def check_dates(self):
    if self.target_date is not None and self.start_date >= self.target_date:
      raise ValueError("target_dateはstart_dateよりも後でなければならない")
    return self

class GoalsTasksOut(BaseModel):
  goal_name: str = Field(max_length=50)
  deadline: datetime.date
  estimated_time: float
  status: GoalsTasksStatus = GoalsTasksStatus.Todo