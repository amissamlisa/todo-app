import datetime
from unittest import TestCase

from backend.models.models import GoalsTasks, GoalsTasksStatusEnum


class GoalTaskTest(TestCase):
    def _task(self, **kwargs):
        defaults = dict(
            goal_task_name="英単語帳を暗記",
            order_num=1,
            deadline=datetime.date(2030, 10, 15),
            goal_task_status="作業中",
            estimated_time=180,
        )
        defaults.update(kwargs)
        return GoalsTasks(**defaults)

    def test_goal_task_sets_all_fields_correctly(self):
        goal_task = self._task()
        self.assertEqual(
            (
                goal_task.goal_task_name,
                goal_task.order_num,
                goal_task.deadline,
                goal_task.goal_task_status,
                goal_task.estimated_time,
            ),
            (
                "英単語帳を暗記",
                1,
                datetime.date(2030, 10, 15),
                GoalsTasksStatusEnum.InProgress.value,
                180,
            ),
        )

    def test_goal_task_name_trim(self):
        goal_task = self._task(goal_task_name="  英単語帳を暗記  ")
        self.assertEqual(goal_task.goal_task_name, "英単語帳を暗記")

    def test_goal_task_name_remove_fullwidth_space(self):
        goal_task = self._task(goal_task_name="　英単語帳を暗記　")
        self.assertEqual(goal_task.goal_task_name, "英単語帳を暗記")

    def test_goal_task_name_none(self):
        with self.assertRaises(ValueError):
            self._task(goal_task_name=None)

    def test_goal_task_status_none(self):
        with self.assertRaises(ValueError):
            self._task(goal_task_status=None)

    def test_goal_task_with_invalid_status(self):
        with self.assertRaises(ValueError):
            self._task(goal_task_status="未対応")

    def test_deadline_not_date_type(self):
        with self.assertRaises(TypeError):
            self._task(deadline="2030-10-15")

    def test_goal_task_with_valid_status(self):
        goal_task = self._task(goal_task_status="完了")
        self.assertEqual(goal_task.goal_task_status, "完了")
