import datetime

from sqlalchemy import update
from sqlalchemy.orm import Session
from ..models.models import Goals, GoalsStatusEnum, GoalsTasks, GoalsTasksStatusEnum, Users


class GoalRepository:
    def __init__(self):
        pass

    def register_goal(self, db, goal: Goals, commit=True):
        try:
            db.add(goal)
            db.flush()
            if commit:
                db.commit()
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

    def update_goal_status_from_db(self, db: Session, goal_id, commit=True):
        try:
            stmt = (
                update(Goals)
                .where(Goals.status == GoalsStatusEnum.Unachieved, Goals.goal_id == goal_id)
                .values(status=GoalsStatusEnum.Achieved)
            )
            db.execute(stmt)
            if commit:
                db.commit()
        except Exception as e:
            db.rollback()
            raise e


class GoalTaskRepository:
    def __init__(self):
        pass

    def register_goal_task(self, db, goal_task: GoalsTasks, commit=True):
        try:
            db.add(goal_task)
            db.flush()
            if commit:
                db.commit()
            return goal_task
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

    def update_goal_task_stauts_from_db(self, db: Session, goal_task_id, new_goal_task_status: GoalsTasksStatusEnum,
                                        commit=True):
        try:
            curr_goal_task_status = (
                db.query(GoalsTasks.goal_task_status)
                .filter(GoalsTasks.goal_task_id == goal_task_id)
                .scalar()
            )
            if curr_goal_task_status != new_goal_task_status:
                stmt = (
                    update(GoalsTasks)
                    .where(GoalsTasks.goal_task_id == goal_task_id)
                    .values(goal_task_status=new_goal_task_status)
                )
                db.execute(stmt)
                if commit:
                    db.commit()
            else:
                raise ValueError("同じステータスの変更はできません")
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
