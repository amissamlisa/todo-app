import datetime
from unittest import TestCase

from pydantic import ValidationError

from backend.models.models import GoalsTasksStatusEnum
from backend.schemas.schemas import (
    GoalTaskCreateRequest,
    GoalTaskOrderUpdateRequest,
    GoalTaskStatusAndOrderUpdateRequest,
    GoalTaskUpdateRequest,
    GoalRequestWithTasks,
    GoalsRequest,
    GoalsTasksOut,
    SaveRequest,
)


class TestGoalTaskRequest(TestCase):
    def _create_request(self, **kwargs):
        defaults = dict(
            goal_task_name="単語学習",
            deadline=datetime.date(2030, 10, 18),
            estimated_time=60,
            goal_task_status="完了",
        )
        defaults.update(kwargs)
        return GoalTaskCreateRequest(**defaults)

    def _update_request(self, **kwargs):
        defaults = dict(
            goal_task_name="単語学習",
            deadline=datetime.date(2030, 10, 18),
            estimated_time=60,
        )
        defaults.update(kwargs)
        return GoalTaskUpdateRequest(**defaults)

    def _order_update_request(self, **kwargs):
        defaults = dict(
            from_goal_task_id=1,
            to_goal_task_id=2,
            from_goal_task_order=1,
            to_goal_task_order=2,
        )
        defaults.update(kwargs)
        return GoalTaskOrderUpdateRequest(**defaults)

    def _status_order_update_request(self, **kwargs):
        defaults = dict(order_num=1, new_status="完了")
        defaults.update(kwargs)
        return GoalTaskStatusAndOrderUpdateRequest(**defaults)

    def test_goal_task_create_request_with_valid_input(self):
        req = self._create_request()
        self.assertEqual(req.estimated_time, 60)

    def test_goal_task_create_request_with_empty_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._create_request(goal_task_name="")

    def test_goal_task_create_request_with_min_length_name(self):
        self._create_request(goal_task_name="あ")

    def test_goal_task_create_request_with_max_length_name(self):
        self._create_request(goal_task_name="あ" * 100, goal_task_status="未着手")

    def test_goal_task_create_request_with_too_long_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._create_request(goal_task_name="あ" * 101, goal_task_status="未着手")

    def test_goal_task_create_request_with_zero_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._create_request(estimated_time=0, goal_task_status="未着手")

    def test_goal_task_create_request_with_min_estimated_time(self):
        req = self._create_request(estimated_time=1, goal_task_status="未着手")
        self.assertEqual(req.estimated_time, 1)

    def test_goal_task_create_request_with_max_estimated_time(self):
        self._create_request(estimated_time=720, goal_task_status="未着手")

    def test_goal_task_create_request_with_too_large_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._create_request(estimated_time=721, goal_task_status="未着手")

    def test_goal_task_create_request_with_invalid_status_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._create_request(
                estimated_time=721, goal_task_status="不明なステータス"
            )

    def test_goal_task_update_request_with_empty_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._update_request(goal_task_name="")

    def test_goal_task_update_request_with_min_length_name(self):
        self._update_request(goal_task_name="あ")

    def test_goal_task_update_request_with_max_length_name(self):
        self._update_request(goal_task_name="あ" * 100)

    def test_goal_task_update_request_with_too_long_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._update_request(goal_task_name="あ" * 101)

    def test_goal_task_update_request_with_zero_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._update_request(estimated_time=0)

    def test_goal_task_update_request_with_min_estimated_time(self):
        self._update_request(estimated_time=1)

    def test_goal_task_update_request_with_max_estimated_time(self):
        self._update_request(estimated_time=720)

    def test_goal_task_update_request_with_too_large_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._update_request(estimated_time=721)

    def test_goal_task_order_update_request_with_invalid_from_order_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._order_update_request(from_goal_task_order=0)

    def test_goal_task_order_update_request_accepts_valid_payload(self):
        req = self._order_update_request()
        self.assertEqual(req.to_goal_task_id, 2)

    def test_goal_task_order_update_request_with_invalid_from_goal_task_id_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._order_update_request(from_goal_task_id=0)

    def test_goal_task_order_update_request_with_invalid_to_goal_task_id_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._order_update_request(to_goal_task_id=0)

    def test_goal_task_order_update_request_with_invalid_to_order_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._order_update_request(to_goal_task_order=0)

    def test_goal_task_status_and_order_update_request_with_invalid_order_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._status_order_update_request(order_num=0)

    def test_goal_task_status_and_order_update_request_accepts_valid_payload(self):
        req = self._status_order_update_request()
        self.assertEqual(req.new_status.value, "完了")

    def test_goal_task_status_and_order_update_request_with_invalid_status_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._status_order_update_request(new_status="不明")


class TestGoalTaskOutputSchema(TestCase):
    def _task_out(self, **kwargs):
        defaults = dict(
            goal_task_name="単語学習",
            deadline=datetime.date(2030, 10, 18),
            estimated_time=60,
        )
        defaults.update(kwargs)
        return GoalsTasksOut(**defaults)

    def test_goals_tasks_out_accepts_valid_payload(self):
        req = self._task_out()
        self.assertEqual(req.goal_task_name, "単語学習")

    def test_goals_tasks_out_accepts_max_length_name(self):
        with self.assertRaises(ValidationError):
            self._task_out(goal_task_name="")

    def test_goals_tasks_out_accepts_max_length_name(self):
        req = self._task_out(goal_task_name="あ")
        self.assertEqual(len(req.goal_task_name), 100)

    def test_goals_tasks_out_accepts_max_length_name(self):
        req = self._task_out(goal_task_name="あ" * 100)
        self.assertEqual(len(req.goal_task_name), 100)

    def test_goals_tasks_out_with_too_long_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            self._task_out(goal_task_name="あ" * 101)

    def test_goal_task_update_request_with_zero_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._task_out(estimated_time=0)

    def test_goals_tasks_out_accepts_min_estimated_time(self):
        req = self._task_out(estimated_time=1)
        self.assertEqual(req.estimated_time, 1)

    def test_goals_tasks_out_accepts_max_estimated_time(self):
        req = self._task_out(estimated_time=720)
        self.assertEqual(req.estimated_time, 720)

    def test_goals_tasks_out_with_too_large_estimated_time_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            self._task_out(estimated_time=721)


class TestGoalCompositeSchema(TestCase):
    def _goal(self):
        return GoalsRequest(
            goal_name="TOEIC800点取得",
            status_against_goal="現在TOEIC400点",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            weekday_available_time=90,
            weekends_available_time=180,
            task_creation_rule="リーディングを中心にしたい",
        )

    def _completed_task(self):
        return GoalsTasksOut(
            goal_task_name="単語学習",
            deadline=datetime.date(2030, 10, 18),
            estimated_time=60,
            goal_task_status=GoalsTasksStatusEnum.Completed.value,
        )

    def _incomplete_task(self):
        return GoalsTasksOut(
            goal_task_name="単語学習",
            deadline=datetime.date(2030, 10, 18),
            estimated_time=60,
            goal_task_status=GoalsTasksStatusEnum.Todo.value,
        )

    def test_goal_request_with_tasks_accepts_valid_payload(self):
        req = GoalRequestWithTasks(
            goal=self._goal(),
            completed_goal_tasks_list=[self._completed_task()],
        )
        self.assertEqual(len(req.completed_goal_tasks_list), 1)

    def test_goal_request_with_tasks_rejects_non_completed_status(self):
        with self.assertRaises(ValidationError):
            GoalRequestWithTasks(
                goal=self._goal(),
                completed_goal_tasks_list=[self._incomplete_task()],
            )

    def test_goal_request_with_tasks_accepts_none_completed_goal_tasks_list(self):
        req = GoalRequestWithTasks(goal=self._goal())
        self.assertIsNone(req.completed_goal_tasks_list)

    def test_goal_request_with_tasks_accepts_completed_task_with_past_deadline(self):
        req = GoalRequestWithTasks(
            goal=self._goal(),
            completed_goal_tasks_list=[
                {
                    "goal_task_name": "過去に完了したタスク",
                    "deadline": "2026-04-20",
                    "estimated_time": 30,
                    "goal_task_status": "完了",
                }
            ],
        )
        self.assertEqual(len(req.completed_goal_tasks_list), 1)

    def test_save_request_accepts_valid_payload(self):
        req = SaveRequest(
            goal=self._goal(),
            goal_tasks=[self._incomplete_task()],
            goal_total_estimated_time=60,
        )
        self.assertEqual(req.goal_total_estimated_time, 60)

    def test_save_request_with_zero_total_estimated_time_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            SaveRequest(
                goal=self._goal(),
                goal_tasks=[self._completed_task()],
                goal_total_estimated_time=0,
            )
