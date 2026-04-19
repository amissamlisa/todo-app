import datetime
from unittest import TestCase

from pydantic import ValidationError

from backend.models.models import GoalsStatusEnum
from backend.schemas.schemas import GoalsRequest


class TestGoalsRequest(TestCase):
    def _valid_payload(self, **kwargs):
        defaults = dict(
            goal_name="TOEIC800点取得",
            status_against_goal="現在400点",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            weekday_available_time=90,
            weekends_available_time=180,
            task_creation_rule="リーディングを中心にしたい",
        )
        defaults.update(kwargs)
        return defaults

    def test_goals_request_accepts_valid_payload(self):
        req = GoalsRequest(**self._valid_payload())
        self.assertEqual(req.goal_name, "TOEIC800点取得")

    def test_goals_request_applies_default_status(self):
        req = GoalsRequest(**self._valid_payload())
        self.assertEqual(req.status, GoalsStatusEnum.Unachieved.value)

    def test_goals_request_accepts_none_task_creation_rule(self):
        req = GoalsRequest(**self._valid_payload(task_creation_rule=None))
        self.assertIsNone(req.task_creation_rule)

    def test_goals_request_with_too_short_goal_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(goal_name=""))

    def test_goals_request_with_too_long_goal_name_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(goal_name="あ" * 101))

    def test_goals_request_with_too_short_status_against_goal_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(status_against_goal=""))

    def test_goals_request_with_too_long_status_against_goal_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(status_against_goal="あ" * 201))


    def test_goals_request_with_start_day_after_target_day_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(
                **self._valid_payload(
                    start_day=datetime.date(2030, 10, 23),
                    target_day=datetime.date(2030, 10, 22),
                )
            )
    def test_goals_request_with_start_day_before_today_raises_validation_error(
        self,
    ):
        today = datetime.date.today()
        with self.assertRaises(ValidationError):
            GoalsRequest(
                **self._valid_payload(
                    start_day=today - datetime.timedelta(days=1),
                    target_day=datetime.date(2030, 10, 22),
                )
            )

    def test_goals_request_with_start_day_today_raises_validation_error(self):
        today = datetime.date.today()
        with self.assertRaises(ValidationError):
            GoalsRequest(
                **self._valid_payload(
                    start_day=today,
                    target_day=today + datetime.timedelta(days=1),
                )
            )

    def test_goals_request_with_target_day_today_raises_validation_error(self):
        today = datetime.date.today()
        with self.assertRaises(ValidationError):
            GoalsRequest(
                **self._valid_payload(
                    start_day=today + datetime.timedelta(days=1),
                    target_day=today,
                )
            )

    def test_goals_request_with_target_day_within_three_months_is_valid(self):
        req = GoalsRequest(
            **self._valid_payload(
                start_day=datetime.date(2030, 1, 15),
                target_day=datetime.date(2030, 4, 15),
            )
        )
        self.assertEqual(req.target_day, datetime.date(2030, 4, 15))

    def test_goals_request_with_target_day_over_three_months_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(
                **self._valid_payload(
                    start_day=datetime.date(2030, 1, 15),
                    target_day=datetime.date(2030, 4, 16),
                )
            )

    def test_goals_request_with_weekday_available_time_below_min_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(weekday_available_time=0))

    def test_goals_request_with_weekends_available_time_above_max_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(weekday_available_time=721))
    
    def test_goals_request_with_weekends_available_time_below_min_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(weekends_available_time=0))

    def test_goals_request_with_weekends_available_time_above_max_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(weekends_available_time=721))

    def test_goals_request_with_too_long_task_creation_rule_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            GoalsRequest(**self._valid_payload(task_creation_rule="あ" * 801))
