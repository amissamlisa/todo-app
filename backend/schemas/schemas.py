from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Optional, List
import datetime
import re

from backend.models.models import GoalsStatusEnum, GoalsTasksStatusEnum


class GoalsRequest(BaseModel):
    goal_name: str = Field(max_length=100)
    status_against_goal: str = Field(max_length=200)
    start_day: datetime.date
    target_day: datetime.date
    status: str = GoalsStatusEnum.Unachieved.value
    weekday_available_time: int = Field(ge=1, le=720)
    weekends_available_time: int = Field(ge=1, le=720)
    task_creation_rule: Optional[str] = Field(default=None, max_length=800)

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_day > self.target_day:
            raise ValueError("target_dayはstart_dayよりも後でなければならない")
        return self


class GoalsTasksOut(BaseModel):
    goal_task_name: str = Field(max_length=100)
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)


class GoalRequestWithTasks(BaseModel):
    goal: GoalsRequest
    goal_tasks_list: Optional[List[GoalsTasksOut]] = None


class SaveRequest(BaseModel):
    goal: GoalsRequest
    goal_tasks: list[GoalsTasksOut]
    goal_total_estimated_time: int = Field(ge=1)


class GoalTaskOrderUpdateRequest(BaseModel):
    from_goal_task_id: int
    to_goal_task_id: int
    from_goal_task_order: int = Field(ge=1)
    to_goal_task_order: int = Field(ge=1)


class GoalTaskUpdateRequest(BaseModel):
    goal_task_name: str
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)


class GoalTaskCreateRequest(BaseModel):
    goal_task_name: str = Field(min_length=1, max_length=100)
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)
    goal_task_status: GoalsTasksStatusEnum


class GoalTaskStatusAndOrderUpdateRequest(BaseModel):
    order_num: int = Field(ge=1)
    new_status: GoalsTasksStatusEnum


class UserRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=10)
    confirmation_password: str = Field(min_length=10)
    email: EmailStr

    @model_validator(mode="after")
    def check_password(self):
        pw = self.password
        cpw = self.confirmation_password

        pattern = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z0-9\W_]{10,}$"

        if re.match(pattern, pw) is None:
            raise ValueError("大・小英数字・記号がそれぞれ1文字ずつ含まれていません")

        if pw != cpw:
            raise ValueError("パスワードと確認パスワードが一致しません")
        return self


class UserPointsUpdateRequest(BaseModel):
    points: int = Field(ge=0)


class PasswordResetEmailRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    password: str = Field(min_length=10)
    token: str | None


class Token(BaseModel):
    access_token: str
    token_type: str