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

    def register_goal_task(self, db, goal_tasks: List[GoalsTasks], commit=True):
        try:
            db.add_all(goal_tasks)
            db.flush()
            if commit:
                db.commit()
            return goal_tasks
        except Exception as e:
            db.rollback()
            raise e

    def delete_goal_task_from_db(self, db: Session, goal: GoalsTasks, commit=True):
        try:
            db.delete(goal)
            if commit:
                db.commit()
        except Exception as e:
            db.rollback()
            raise e

    def update_goal_task_status_from_db(
        self,
        db: Session,
        goal_task_id,
        new_goal_task_status: GoalsTasksStatusEnum,
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
                if commit:
                    db.commit()
                    db.refresh(goal_task)
                return goal_task
            else:
                raise StatusUnchangedError("目標達成タスク")
        except Exception as e:
            db.rollback()
            raise e


class UserRepository:
    def __init__(self):
        pass

    def find_user_by_email(self, db: Session, email: str):
        user = db.query(Users).filter(Users.email == email).first()
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

    def disable_refresh_token(
        self, db: Session, refresh_token: RefreshTokens, user_id: int, commit=True
    ):
        try:
            refresh_token = (
                db.query(RefreshTokens).filter(RefreshTokens.user_id == user_id).all()
            )
            for refresh_token in refresh_token:
                refresh_token.revoked_at = datetime.now(timezone.utc)
            if commit:
                db.commit()
                return refresh_token
        except Exception as e:
            db.rollback()
            raise e

    def revoke_refresh_token(self, db: Session, token_id: int, commit=True):
        try:
            token = (
                db.query(RefreshTokens)
                .filter(RefreshTokens.refresh_token_id == token_id)
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
