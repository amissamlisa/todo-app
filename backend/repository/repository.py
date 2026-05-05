from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session
from ..models.models import (
    Goals,
    GoalsStatusEnum,
    GoalsTasks,
    GoalsTasksStatusEnum,
    PasswordResetTokens,
    Users,
    RefreshTokens,
)


class EmailAlreadyRegistered(Exception):
    def __str__(self):
        return "既に同じメールアドレスが登録されています"


class UnachievedGoalAlreadyExists(Exception):
    def __str__(self):
        return "未達成のゴールが存在します"


class GoalNotFound(Exception):
    def __str__(self):
        return "目標が見つかりません"


class GoalTaskNotFound(Exception):
    def __str__(self):
        return "目標達成タスクが見つかりません"


class StatusUnchangedError(Exception):
    def __str__(self):
        return f"現在の{self.args[0]}ステータスと同じステータスのため、変更できません"


class AchievedStatusImmutable(Exception):
    def __str__(self):
        return "達成から未達成へ目標ステータスを変更できません"


class GoalRepository:
    def __init__(self):
        pass

    def search_goal_by_user_id(self, db, user_id: int):
        goals = (
            db.query(Goals)
            .filter(
                Goals.user_id == user_id,
                Goals.status == GoalsStatusEnum.Unachieved.value,
            )
            .all()
        )
        return goals

    def fetch_goal_by_id_from_db(self, db: Session, goal_id: int):
        return db.query(Goals).filter(Goals.goal_id == goal_id).first()

    def register_goal(self, db, goal: Goals, commit=True):
        try:
            existing_goal = (
                db.query(Goals)
                .filter(
                    Goals.status == GoalsStatusEnum.Unachieved.value,
                    Goals.user_id == goal.user_id,
                )
                .first()
            )
            if existing_goal:
                raise UnachievedGoalAlreadyExists()
            db.add(goal)
            db.flush()
            if commit:
                db.commit()
                db.refresh(goal)
            return goal
        except Exception as e:
            db.rollback()
            raise e

    def delete_goal_from_db(self, db: Session, goal: Goals, commit=True):
        try:
            db.delete(goal)
            if commit:
                db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_from_db(self, db: Session, new_goal: Goals, commit=True):
        try:
            if new_goal.status != GoalsStatusEnum.Unachieved.value:
                raise ValueError("無効な目標ステータスです")

            existing_goal = (
                db.query(Goals)
                .filter(
                    Goals.user_id == new_goal.user_id,
                    Goals.status == GoalsStatusEnum.Unachieved.value,
                )
                .first()
            )
            if existing_goal is None:
                raise GoalNotFound()

            existing_goal.status_against_goal = new_goal.status_against_goal
            existing_goal.start_day = new_goal.start_day
            existing_goal.target_day = new_goal.target_day
            existing_goal.weekday_available_time = new_goal.weekday_available_time
            existing_goal.weekends_available_time = new_goal.weekends_available_time
            existing_goal.total_estimated_time = new_goal.total_estimated_time
            existing_goal.task_creation_rule = new_goal.task_creation_rule
            existing_goal.status = new_goal.status
            if commit:
                db.commit()
                db.refresh(existing_goal)
            return existing_goal
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_status_from_db(
        self, db: Session, goal_id, new_goal_status, commit=True
    ):
        try:
            goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
            if goal is None:
                raise GoalNotFound()
            # ステータス更新
            if new_goal_status not in [
                GoalsStatusEnum.Unachieved,
                GoalsStatusEnum.Achieved,
            ]:
                raise ValueError("無効な目標ステータスです")
            if (
                new_goal_status.value == GoalsStatusEnum.Unachieved.value
                and goal.status == GoalsStatusEnum.Achieved.value
            ):
                raise AchievedStatusImmutable()
            if goal.status != new_goal_status.value:
                goal.status = new_goal_status.value
                if commit:
                    db.commit()
                    db.refresh(goal)
                return goal
            else:
                raise StatusUnchangedError("目標")
        except Exception as e:
            db.rollback()
            raise e


class GoalTaskRepository:
    def __init__(self):
        pass

    def get_goal_task_by_goal_task_id_from_db(self, db: Session, goal_task_id: int):
        return (
            db.query(GoalsTasks).filter(GoalsTasks.goal_task_id == goal_task_id).first()
        )

    def get_goal_task_by_goal_id(self, db, goal_id: int):
        goal_tasks = (
            db.query(GoalsTasks)
            .filter(
                GoalsTasks.goal_id == goal_id,
            )
            .first()
        )
        return goal_tasks

    def fetch_goal_tasks_by_goal_id_from_db(self, db: Session, goal_id: int):
        return (
            db.query(GoalsTasks)
            .filter(GoalsTasks.goal_id == goal_id)
            .order_by(GoalsTasks.order_num.asc(), GoalsTasks.goal_task_id.asc())
            .all()
        )

    def register_goal_task(self, db, goal_tasks: List[GoalsTasks], commit=True):
        try:
            for index, task in enumerate(goal_tasks, start=1):
                if task.order_num is None:
                    task.order_num = index
            db.add_all(goal_tasks)
            db.flush()
            if commit:
                db.commit()
            return goal_tasks
        except Exception as e:
            db.rollback()
            raise e

    def delete_goal_task_from_db(
        self, db: Session, goal_tasks: GoalsTasks, commit=True
    ):
        try:
            db.delete(goal_tasks)
            if commit:
                db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def replace_goal_tasks_from_db(
        self, db: Session, goal_id: int, goal_tasks: List[GoalsTasks], commit=True
    ):
        try:
            existing_goal_tasks = (
                db.query(GoalsTasks).filter(GoalsTasks.goal_id == goal_id).all()
            )
            for task in existing_goal_tasks:
                db.delete(task)

            for index, task in enumerate(goal_tasks, start=1):
                if task.order_num is None:
                    task.order_num = index
            db.add_all(goal_tasks)
            db.flush()

            if commit:
                db.commit()
            return goal_tasks
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_task_status_and_order_from_db(
        self,
        db: Session,
        goal_task_id,
        new_goal_task_status: GoalsTasksStatusEnum,
        order_num: int,
        commit=True,
    ):
        try:
            goal_task = (
                db.query(GoalsTasks)
                .filter(GoalsTasks.goal_task_id == goal_task_id)
                .first()
            )
            if goal_task is None:
                raise GoalTaskNotFound()

            # ステータス更新
            if goal_task.goal_task_status != new_goal_task_status.value:
                goal_task.goal_task_status = new_goal_task_status.value
                goal_task.order_num = order_num
                if commit:
                    db.commit()
                    db.refresh(goal_task)
                return goal_task
            else:
                raise StatusUnchangedError("目標達成タスク")
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_task_order_from_db(
        self,
        db: Session,
        from_goal_task_id: int,
        to_goal_task_id: int,
        commit=True,
    ):
        try:
            from_goal_task = (
                db.query(GoalsTasks)
                .filter(GoalsTasks.goal_task_id == from_goal_task_id)
                .first()
            )
            if from_goal_task is None:
                raise GoalTaskNotFound()

            to_goal_task = (
                db.query(GoalsTasks)
                .filter(GoalsTasks.goal_task_id == to_goal_task_id)
                .first()
            )
            if to_goal_task is None:
                raise GoalTaskNotFound()

            if from_goal_task.goal_id != to_goal_task.goal_id:
                raise ValueError("同じ目標内のタスクのみ並び替えできます")

            goal_tasks = (
                db.query(GoalsTasks)
                .filter(GoalsTasks.goal_id == from_goal_task.goal_id)
                .order_by(GoalsTasks.order_num.asc(), GoalsTasks.goal_task_id.asc())
                .all()
            )

            from_index = None
            for i, task in enumerate(goal_tasks):
                if task.goal_task_id == from_goal_task_id:
                    from_index = i
                    break

            to_index = None
            for i, task in enumerate(goal_tasks):
                if task.goal_task_id == to_goal_task_id:
                    to_index = i
                    break

            if from_index is None or to_index is None:
                raise GoalTaskNotFound()
            if from_index == to_index:
                raise StatusUnchangedError("目標達成タスク")

            moved_task = goal_tasks.pop(from_index)
            goal_tasks.insert(to_index, moved_task)

            for index, task in enumerate(goal_tasks, start=1):
                task.order_num = index

            db.flush()

            if commit:
                db.commit()
                db.refresh(from_goal_task)
                db.refresh(to_goal_task)
            return from_goal_task, to_goal_task
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_task_from_db(
        self,
        db: Session,
        goal_task_id: int,
        goal_task_name: str,
        deadline: datetime.date,
        estimated_time: int,
        commit=True,
    ):
        try:
            goal_task = (
                db.query(GoalsTasks)
                .filter(GoalsTasks.goal_task_id == goal_task_id)
                .first()
            )
            if goal_task is None:
                raise GoalTaskNotFound()

            goal_task.goal_task_name = goal_task_name
            goal_task.deadline = deadline
            goal_task.estimated_time = estimated_time

            if commit:
                db.commit()
                db.refresh(goal_task)
            return goal_task
        except Exception as e:
            db.rollback()
            raise e


class UserRepository:
    def __init__(self):
        pass

    def find_user_by_email(self, db: Session, email: str):
        user = db.query(Users).filter(Users.email == email).first()
        return user

    def find_user_by_user_id(self, db: Session, user_id: int):
        user = db.query(Users).filter(Users.user_id == user_id).first()
        return user

    def register_user(self, db: Session, user: Users, commit=True):
        try:
            existing_email = db.query(Users).filter(Users.email == user.email).first()
            if existing_email:
                raise EmailAlreadyRegistered()
            db.add(user)
            db.flush()
            if commit:
                db.commit()
                return user

        except Exception as e:
            db.rollback()
            raise e

    def update_user_points_from_db(self, db: Session, user_id, new_points, commit=True):
        try:
            user = db.query(Users).filter(Users.user_id == user_id).first()
            if user is None:
                return None
            user.user_points = new_points
            if commit:
                db.commit()
                return user
        except Exception as e:
            db.rollback()
            raise e

    def update_user_rank_from_db(
        self, db: Session, user_id, new_user_rank, commit=True
    ):
        try:
            user = db.query(Users).filter(Users.user_id == user_id).first()
            if user is None:
                return None
            user.user_rank = new_user_rank
            if commit:
                db.commit()
                return user
        except Exception as e:
            db.rollback()
            raise e

    def update_user_from_db(self, db: Session, user_id, new_data, commit=True):
        try:
            user = db.query(Users).filter(Users.user_id == user_id).first()
            user.username = new_data.username
            user.email = new_data.email
            user.hashed_password = new_data.hashed_password
            if commit:
                db.commit()
                return user
        except Exception as e:
            db.rollback()
            raise e


class RefreshTokenRepository:
    def __init__(self):
        pass

    def register_refresh_token(
        self, db: Session, refresh_token: RefreshTokens, commit=True
    ):
        try:
            db.add(refresh_token)
            db.flush()
            if commit:
                db.commit()
            return refresh_token
        except Exception as e:
            db.rollback()
            raise e

    def revoke_refresh_token(self, db: Session, refresh_token_id: int, commit=True):
        try:
            token = (
                db.query(RefreshTokens)
                .filter(RefreshTokens.refresh_token_id == refresh_token_id)
                .first()
            )
            if token:
                token.revoked_at = datetime.now(timezone.utc)
            if commit:
                db.commit()
            return token
        except Exception as e:
            db.rollback()
            raise e

    def revoke_all_user_tokens(self, db: Session, user_id: int, commit=True):
        try:
            tokens = (
                db.query(RefreshTokens)
                .filter(
                    RefreshTokens.user_id == user_id, RefreshTokens.revoked_at.is_(None)
                )
                .all()
            )
            for token in tokens:
                token.revoked_at = datetime.now(timezone.utc)
            if commit:
                db.commit()
            return len(tokens)
        except Exception as e:
            db.rollback()
            raise e

    def delete_expired_refresh_tokens(
        self, db: Session, now: datetime | None = None, commit=True
    ):
        try:
            if now is None:
                now = datetime.now(timezone.utc)
            deleted_count = (
                db.query(RefreshTokens)
                .filter(RefreshTokens.expires_at < now)
                .delete(synchronize_session=False)
            )
            if commit:
                db.commit()
            return deleted_count
        except Exception as e:
            db.rollback()
            raise e


class PasswordResetRepository:
    def __init__(self):
        pass

    def register_password_reset_token(
        self, db: Session, password_reset: PasswordResetTokens, commit=True
    ):
        try:
            db.add(password_reset)
            db.flush()
            if commit:
                db.commit()
            return password_reset
        except Exception as e:
            db.rollback()
            raise e

    def delete_password_reset_token(
        self, db: Session, password_reset: PasswordResetTokens, commit=True
    ):
        try:
            db.delete(password_reset)
            if commit:
                db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def delete_expired_password_reset_tokens(
        self, db: Session, now: datetime | None = None, commit=True
    ):
        try:
            if now is None:
                now = datetime.now(timezone.utc)
            deleted_count = (
                db.query(PasswordResetTokens)
                .filter(PasswordResetTokens.expires_at < now)
                .delete(synchronize_session=False)
            )
            if commit:
                db.commit()
            return deleted_count
        except Exception as e:
            db.rollback()
            raise e

    def get_password_refresh_token_by_prefix(
        self, db: Session, password_reset_token_prefix
    ):
        return (
            db.query(PasswordResetTokens)
            .filter(PasswordResetTokens.token_prefix == password_reset_token_prefix)
            .all()
        )

    def update_password_from_db(
        self, db: Session, user_id, new_hashed_password, commit=True
    ):
        try:
            user = db.query(Users).filter(Users.user_id == user_id).first()
            user.hashed_password = new_hashed_password
            if commit:
                db.commit()
                return user
        except Exception as e:
            db.rollback()
            raise e
