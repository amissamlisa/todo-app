from pydantic import BaseModel, Field, model_validator
from typing import Optional
from enum import Enum
import datetime
from decimal import Decimal
from typing import List

class GoalsTasksStatus(Enum):
  Todo = "未着手"
  InProgress = "作業中"
  Completed = "完了"

class GoalsTasksRequest(BaseModel):
  goal_name: str = Field(max_length=50)
  status_against_goal: str = Field(max_length=200)
  start_date: datetime.date
  target_date: datetime.date
  weekday_available_hours: Decimal = Field(ge=Decimal("0.0"), le=Decimal("999.9"))
  weekends_available_hours: Decimal = Field(ge=Decimal("0.0"), le=Decimal("999.9"))
  task_creation_rule: Optional[str] = Field(max_length=800)

  @model_validator(mode="after")
  def check_dates(self):
    if self.start_date >= self.target_date:
      raise ValueError("target_dateはstart_dateよりも後でなければならない")
    return self

class GoalsTasksOut(BaseModel):
  goal_task_name: str = Field(max_length=50)
  deadline: datetime.date
  estimated_time: Decimal = Field(ge=Decimal("0.0"), le=Decimal("999.9"))
  status: GoalsTasksStatus = GoalsTasksStatus.Todo

class DailyTasksRequest(BaseModel):
  daily_task_name: str = Field(max_length=50)
  deadline: datetime.date
  estimated_time: Decimal = Field(ge=Decimal("0.0"), le=Decimal("999.9"))

class UserRequest(BaseModel):
  user_name: str = Field(min_length=50)
  password: str = Field(min_length=10)
  confirmation_password: str = Field(min_length=10)
  email: str = Field(max_length=254)


class GoalsTasksListOut(BaseModel):
  goal_task: List[GoalsTasksOut]