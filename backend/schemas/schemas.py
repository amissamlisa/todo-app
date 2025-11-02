from pydantic import BaseModel, Field, model_validator, EmailStr, field_validator
from typing import Optional
from enum import Enum
import datetime
from decimal import Decimal
from typing import List
import re


class GoalsTasksStatus(Enum):
    Todo = "未着手"
    InProgress = "作業中"
    Completed = "完了"


class GoalsTasksRequest(BaseModel):
    goal_name: str = Field(max_length=100)
    status_against_goal: str = Field(max_length=200)
    start_date: datetime.date
    target_date: datetime.date
    weekday_available_hours: Decimal = Field(ge=Decimal("0.1"), le=Decimal("999.9"))
    weekends_available_hours: Decimal = Field(ge=Decimal("0.1"), le=Decimal("999.9"))
    task_creation_rule: Optional[str] = Field(max_length=800)

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.target_date:
            raise ValueError("target_dateはstart_dateよりも後でなければならない")
        return self


class GoalsTasksOut(BaseModel):
    goal_task_name: str = Field(max_length=50)
    deadline: datetime.date
    estimated_time: Decimal = Field(ge=Decimal("0.1"), le=Decimal("999.9"))
    status: GoalsTasksStatus = GoalsTasksStatus.Todo


class GoalsTasksListOut(BaseModel):
    goal_task: List[GoalsTasksOut]


class UserRequest(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=10)
    confirmation_password: str = Field(min_length=10)
    email: EmailStr

    @model_validator(mode='after')
    @classmethod
    def check_password(cls, values):
        pw = values.get('password')
        cpw = values.get('confirmation_password')

        pattern = r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z0-9\W_]{10,}$'

        if re.match(pattern, values) is None:
            raise ValueError('大・小英数字・記号がそれぞれ1文字ずつ含まれていません')

        if pw != cpw:
            raise ValueError("パスワードと確認パスワードが一致しません")
        return values

class Token(BaseModel):
    access_token: str
    token_type: str