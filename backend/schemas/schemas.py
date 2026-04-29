from pydantic import BaseModel, Field, model_validator, EmailStr
from typing import Optional, List
import datetime
import re

from backend.models.models import GoalsStatusEnum, GoalsTasksStatusEnum
from backend.utils.add_month import add_days


class GoalsRequest(BaseModel):
    goal_name: str = Field(min_length=1, max_length=100)
    status_against_goal: str = Field(min_length=1, max_length=200)
    start_day: datetime.date
    target_day: datetime.date
    status: str = GoalsStatusEnum.Unachieved.value
    weekday_available_time: int = Field(ge=1, le=720)
    weekends_available_time: int = Field(ge=1, le=720)
    task_creation_rule: Optional[str] = Field(default=None, max_length=800)

    @model_validator(mode="after")
    def check_dates(self):
        today = datetime.date.today()
        max_target_day = add_days(self.start_day, 90)
        if self.start_day > self.target_day:
            raise ValueError("start_dayはtarget_day以前の日付である必要があります")
        if self.start_day <= today:
            raise ValueError("start_dayは明日以降の日付である必要があります")
        if self.target_day <= today:
            raise ValueError("target_dayは明日以降の日付である必要があります")
        if self.target_day > max_target_day:
            raise ValueError("target_dayはstart_dayから3か月以内である必要があります")
        return self


class GoalsTasksOut(BaseModel):
    goal_task_name: str = Field(min_length=1, max_length=100)
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)
    goal_task_status: Optional[GoalsTasksStatusEnum] = None

    @model_validator(mode="after")
    def validate_deadline(self):
        if self.deadline <= datetime.date.today():
            raise ValueError("deadlineは明日以降の日付である必要があります")
        return self


class CompletedGoalTask(BaseModel):
    goal_task_name: str = Field(min_length=1, max_length=100)
    deadline: datetime.date
    estimated_time: int = Field(ge=1, le=720)
    goal_task_status: GoalsTasksStatusEnum


class GoalRequestWithTasks(BaseModel):
    goal: GoalsRequest
    completed_goal_tasks_list: Optional[List[CompletedGoalTask]] = None

    @model_validator(mode="after")
    def validate_completed_tasks(self):
        if self.completed_goal_tasks_list:
            for task in self.completed_goal_tasks_list:
                if task.goal_task_status != GoalsTasksStatusEnum.Completed:
                    raise ValueError(
                        "completed_goal_tasks_list には完了タスクのみ入れてください"
                    )
        return self


class SaveRequest(BaseModel):
    goal: GoalsRequest
    goal_tasks: list[GoalsTasksOut]
    goal_total_estimated_time: int = Field(ge=1)


class GoalTaskOrderUpdateRequest(BaseModel):
    from_goal_task_id: int = Field(ge=1)
    to_goal_task_id: int = Field(ge=1)
    from_goal_task_order: int = Field(ge=1)
    to_goal_task_order: int = Field(ge=1)


class GoalTaskUpdateRequest(BaseModel):
    goal_task_name: str = Field(min_length=1, max_length=100)
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

        if len(pw.encode("utf-8")) > 72:
            raise ValueError("パスワードは72バイト以内で入力してください")

        pattern = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z0-9\W_]{10,}$"

        if re.match(pattern, pw) is None:
            raise ValueError(
                "大・小英字・数字・記号がそれぞれ1文字ずつ含まれていません"
            )

        if pw != cpw:
            raise ValueError("パスワードと確認パスワードが一致しません")
        return self


class UserPointsUpdateRequest(BaseModel):
    points: int = Field(ge=0)


class UserRankUpdateRequest(BaseModel):
    user_rank: str


class PasswordResetEmailRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    password: str = Field(min_length=10)
    token: str

    @model_validator(mode="after")
    def check_password(self):
        pw = self.password
        if len(pw.encode("utf-8")) > 72:
            raise ValueError("パスワードは72バイト以内で入力してください")
        return self


class Token(BaseModel):
    access_token: str
    token_type: str
