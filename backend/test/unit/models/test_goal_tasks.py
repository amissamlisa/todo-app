import datetime
from unittest import TestCase

from backend.models.models import GoalsTasks, GoalsTasksStatusEnum


class GoalTaskTest(TestCase):
    # 初期化時に値が正しく設定された場合
    def test_create_goal_with_todo_status(self):
        goal_task = GoalsTasks(
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            goal_task_status=GoalsTasksStatusEnum.InProgress.value,
            estimated_time=180,
        )

        self.assertEqual(goal_task.goal_task_name, "英単語帳を暗記",
                         "goal_task_nameの値が一致しません")
        self.assertEqual(goal_task.deadline, datetime.date(2030, 10, 15),
                         "deadlineの値が一致しません")
        self.assertEqual(goal_task.goal_task_status,GoalsTasksStatusEnum.InProgress.value)
        self.assertEqual(goal_task.estimated_time, 180,
                         "estimated_timeの値が一致しません")