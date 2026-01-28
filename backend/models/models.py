from sqlalchemy import String, ForeignKey, Date, DateTime, CheckConstraint, Integer
import enum
from sqlalchemy.sql import func
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, validates
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
import datetime
import jpholiday


class GoalsTasksStatusEnum(enum.Enum):
    Todo = "未着手"
    InProgress = "作業中"
    Completed = "完了"


class GoalsStatusEnum(enum.Enum):
    Unachieved = "未達成"
    Achieved = "達成"


class Base(DeclarativeBase):
    pass


class Goals(Base):
    __tablename__ = "goals"

    goal_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    goal_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(default=GoalsStatusEnum.Unachieved.value, nullable=False)
    start_day: Mapped[Date] = mapped_column(Date, nullable=False)
    target_day: Mapped[Date] = mapped_column(Date, nullable=False)
    status_against_goal: Mapped[str] = mapped_column(String(200), nullable=False)
    weekday_available_time: Mapped[int] = mapped_column(Integer, nullable=False)
    weekends_available_time: Mapped[int] = mapped_column(Integer, nullable=False)
    total_estimated_time: Mapped[int] = mapped_column(Integer, nullable=False)
    task_creation_rule: Mapped[str | None] = mapped_column(String(800))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    __table_args__ = (
        CheckConstraint("length(goal_name) > 0", name="check_goal_name_greater_than_zero"),
        CheckConstraint('start_day <= target_day', name='check_start_before_target'),
        CheckConstraint('start_day > CURRENT_DATE', name='check_start_before_now'),
        CheckConstraint('target_day > CURRENT_DATE', name='check_target_before_now'),
        CheckConstraint('length(status_against_goal) > 0', name="check_status_against_goal_greater_than_zero"),
        CheckConstraint('weekday_available_time > 0', name="check_weekday_available_time_greater_than_zero"),
        CheckConstraint('weekends_available_time > 0', name="check_weekends_available_time_greater_than_zero"),
        CheckConstraint('weekday_available_time <= 720', name="check_weekday_available_time_greater_than_720"),
        CheckConstraint('weekends_available_time <= 720', name="check_weekends_available_time_greater_than_720"),
        CheckConstraint('total_estimated_time > 0', name="check_total_estimated_time_greater_than_zero"),
    )

    @validates('goal_name', 'status_against_goal')
    def validate_goal_name(self, key, value: str) -> str:
        if value is None:
            raise ValueError("値がNoneです")
        cleaned = value.strip().replace('\u3000', '')
        return cleaned

    @validates('start_day', 'target_day')
    def validate_date(self, key, value):
        if not isinstance(value, datetime.date):
            raise TypeError("日付はDate型でなければいけません")
        return value

    @validates('status')
    def validate_status(self, key, value: str) -> str:
        valid_values = [GoalsStatusEnum.Unachieved.value, GoalsStatusEnum.Achieved.value]
        if value not in valid_values:
            raise ValueError("無効な目標ステータスです")
        return value

    def calculate_total_estimated_time(self):
        weekday_count = 0
        weekends_count = 0
        holiday_count = 0

        current_day: datetime.date = self.start_day
        while current_day <= self.target_day:
            if jpholiday.is_holiday(current_day):
                holiday_count += self.weekends_available_time
            elif current_day.weekday() < 5:
                weekday_count += self.weekday_available_time
            else:
                weekends_count += self.weekends_available_time
            current_day += datetime.timedelta(days=1)
        total_estimated_time = weekends_count + weekday_count + holiday_count

        return total_estimated_time


class GoalsTasks(Base):
    __tablename__ = "goals_tasks"

    goal_task_id: Mapped[int] = mapped_column(primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.goal_id"), nullable=False)
    goal_task_name: Mapped[str] = mapped_column(String(50), nullable=False)
    goal_task_status: Mapped[str] = mapped_column(default=GoalsTasksStatusEnum.Todo.value, nullable=False)
    deadline: Mapped[Date] = mapped_column(Date, nullable=False)
    estimated_time: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    __table_args__ = (
        CheckConstraint("length(goal_task_name) > 0", name="check_goal_task_name_greater_than_zero"),
        CheckConstraint('deadline > CURRENT_DATE', name='check_deadline_before_now'),
        CheckConstraint('estimated_time > 0', name="check_estimated_time_greater_than_zero"),
        CheckConstraint('estimated_time <= 720', name="check_estimated_time_greater_than_1440"),
    )

    @validates('goal_task_name')
    def validate_goal_name(self, key, value: str) -> str:
        if value is None:
            raise ValueError("値がNoneです")
        cleaned = value.strip().replace('\u3000', '')
        return cleaned

    @validates('goal_task_status')
    def validate_goal_task_status(self, key, value: str) -> str:
        valid_values = [GoalsTasksStatusEnum.Todo.value, GoalsTasksStatusEnum.InProgress.value,
                        GoalsTasksStatusEnum.Completed.value]
        if value not in valid_values:
            raise ValueError("無効な目標達成タスクステータスです")
        return value

    @validates('deadline')
    def validate_date(self, key, value):
        if not isinstance(value, datetime.date):
            raise TypeError("期限はDate型でなければいけません")
        return value


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_points: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    __table_args__ = (
        CheckConstraint("user_points >= 0", name="check_username_more_than_zero"),
    )

    @validates('username')
    def validate_goal_name(self, key, value: str) -> str:
        if value is None:
            raise ValueError("値がNoneです")
        cleaned = value.strip().replace('\u3000', '')
        return cleaned

    @validates('user_points')
    def validate_hour_digits(self, key, value):
        decimal_value = Decimal(str(value))
        if decimal_value.as_tuple().exponent <= -1:
            raise ValueError("小数点の値は無効です")
        return value
    
class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    refresh_token_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    token_prefix: Mapped[str] = mapped_column(String(6), nullable=False)
    hashed_token: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)

class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"
    password_reset_token_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    token_prefix: Mapped[str] = mapped_column(String(6), nullable=False)
    hashed_token: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)