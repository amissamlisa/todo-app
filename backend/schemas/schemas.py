from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Optional, List
import datetime
import re

from backend.models.models import GoalsTasks, Goals


class GoalsRequest(BaseModel):
    goal_name: str = Field(max_length=100)
    status_against_goal: str = Field(max_length=200)
    start_day: datetime.date
    target_day: datetime.date
    weekday_available_time: int = Field(ge=1, le=720)
    weekends_available_time: int = Field(ge=1, le=720)
    total_estimated_time: int = Field(ge=1)
    task_creation_rule: Optional[str] = Field(max_length=800)

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_day >= self.target_day:
            raise ValueError("target_dayはstart_dayよりも後でなければならない")
        return self



class GoalsTasksOut(BaseModel):
    goal_task_name: str = Field(max_length=50)
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)

class GoalRequestWithTasks(BaseModel):
    goal: GoalsRequest
    goal_tasks_list: Optional[List[GoalsTasksOut]] = None



class SaveRequest(BaseModel):
    detail: str
    goal: GoalsRequest
    goal_tasks: list[GoalsTasksOut]

class UserRequest(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=10)
    confirmation_password: str = Field(min_length=10)
    email: EmailStr

    @model_validator(mode='after')
    def check_password(self):
        pw = self.password
        cpw = self.confirmation_password

        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z0-9\W_]{10,}$'

        if re.match(pattern, pw) is None:
            raise ValueError('大・小英数字・記号がそれぞれ1文字ずつ含まれていません')

        if pw != cpw:
            raise ValueError("パスワードと確認パスワードが一致しません")
        return self


class Token(BaseModel):
    access_token: str
    token_type: str