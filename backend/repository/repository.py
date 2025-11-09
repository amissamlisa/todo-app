from typing import List

from sqlalchemy.orm import Session
from ..models.models import Goals, GoalsStatusEnum, GoalsTasks, GoalsTasksStatusEnum, Users


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
        return (
            f"現在の{self.args[0]}ステータスと同じステータスのため、変更できません"
        )


class GoalRepository:
    def __init__(self):
        pass

    def register_goal(self, db, goal: Goals, commit=True):
        try:
            if goal.status not in [GoalsStatusEnum.Unachieved.value, GoalsStatusEnum.Achieved.value]:
                raise ValueError("無効な目標ステータスです")
            existing_goal = db.query(Goals).filter(Goals.status == GoalsStatusEnum.Unachieved.value, Goals.user_id == goal.user_id).first()
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

    def update_goal_status_from_db(self, db: Session, goal_id, new_goal_status, commit=True):
        try:
            goal = db.query(Goals).filter(Goals.goal_id == goal_id).first()
            if goal is None:
                raise GoalNotFound()
            # ステータス更新
            if new_goal_status not in [GoalsStatusEnum.Unachieved, GoalsStatusEnum.Achieved]:
                raise ValueError("無効な目標ステータスです")
            if goal.status != new_goal_status.value and new_goal_status.value != GoalsStatusEnum.Achieved.value:
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

    def update_goal_task_status_from_db(self, db: Session, goal_task_id, new_goal_task_status: GoalsTasksStatusEnum,
                                        commit=True):
        try:
            goal_task = db.query(GoalsTasks).filter(GoalsTasks.goal_task_id == goal_task_id).first()
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

    def register_user(self, db: Session, user: Users, commit=True):
        try:
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