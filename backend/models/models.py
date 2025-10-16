from sqlalchemy import String, ForeignKey, Date, DateTime, Enum, Numeric
import enum
from sqlalchemy.sql import func
from decimal import Decimal 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
import datetime
import jpholiday

PRECISION, SCALE = 4, 1

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
  goal_name: Mapped[str] = mapped_column(String(100), nullable=False)
  status: Mapped[GoalsStatusEnum] = mapped_column(Enum(GoalsStatusEnum), default=GoalsStatusEnum.Unachieved, nullable=False)
  start_day: Mapped[Date] = mapped_column(Date, nullable=False)
  target_day: Mapped[Date] = mapped_column(Date, nullable=False)
  status_against_goal: Mapped[str] = mapped_column(String(200), nullable=False)
  weekday_available_hours: Mapped[Decimal] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
  weekends_available_hours: Mapped[Decimal] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
  total_estimated_time: Mapped[Decimal] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
  task_creation_rule: Mapped[str | None] = mapped_column(String(800))
  created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)


  def calculate_total_estimated_time(self):
    weekday_count = Decimal(0)
    weekends_count = Decimal(0)
    holiday_count = Decimal(0)

    current_day: datetime.date = self.start_day
    while current_day <= self.target_day:
      if jpholiday.is_holiday(current_day):
        holiday_count += self.weekends_available_hours
      elif current_day.weekday() < 5:
        weekday_count += self.weekday_available_hours
      else:
        weekends_count += self.weekends_available_hours
      current_day += datetime.timedelta(days=1)
    total_estimated_time =  weekends_count + weekday_count + holiday_count

    return total_estimated_time

class GoalsTasks(Base):
  __tablename__ = "goals_tasks"

  goal_task_id: Mapped[int] = mapped_column(primary_key=True)
  goal_id: Mapped[int] = mapped_column(ForeignKey("goals.goal_id"), nullable=False)
  goal_task_name: Mapped[str] = mapped_column(String(50), nullable=False)
  goal_task_status: Mapped[GoalsTasksStatusEnum] = mapped_column(Enum(GoalsTasksStatusEnum), default=GoalsTasksStatusEnum.Todo, nullable=False)
  deadline: Mapped[Date] = mapped_column(Date, nullable=False)
  estimated_time: Mapped[Decimal] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
  created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)

class DailyTasks(Base):
  __tablename__ = "daily_tasks"
  daily_task_id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
  daily_task_name: Mapped[str] = mapped_column(String(50), nullable=False)
  goal_task_status: Mapped[GoalsTasksStatusEnum] = mapped_column(Enum(GoalsTasksStatusEnum), default=GoalsTasksStatusEnum.Todo, nullable=False)
  deadline: Mapped[Date] = mapped_column(Date, nullable=False)
  estimated_time: Mapped[Decimal] = mapped_column(Numeric(PRECISION, SCALE), nullable=False)
  created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)

class Users(Base):
  __tablename__ = "users"
  user_id: Mapped[int] = mapped_column(primary_key=True)
  goal_id: Mapped[int] = mapped_column(ForeignKey("goals.goal_id"), nullable=False)
  daily_task_id: Mapped[int] = mapped_column(ForeignKey("daily_tasks.daily_task_id"))
  username: Mapped[str] = mapped_column(String(50), nullable=False)
  hashed_password: Mapped[str] = mapped_column(unique=True, nullable=False)
  email: Mapped[str] = mapped_column(unique=True, nullable=False)
  user_points: Mapped[int] = mapped_column(nullable=True)
  created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)