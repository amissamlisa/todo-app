from unittest import TestCase
import datetime

from psycopg2 import IntegrityError
from backend.models.models import Goals, GoalsStatusEnum


class GoalsTest(TestCase):
    def _goal(self, **kwargs):
        defaults = dict(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=100,
            task_creation_rule="リーディングに重点をおいてタスク生成したい",
        )
        defaults.update(kwargs)
        return Goals(**defaults)

    def test_goal_sets_all_fields_correctly(self):
        goal = self._goal()
        self.assertEqual(
            (
                goal.goal_name,
                goal.start_day,
                goal.target_day,
                goal.weekday_available_time,
                goal.weekends_available_time,
                goal.total_estimated_time,
                goal.task_creation_rule,
            ),
            (
                "TOEIC800点取得",
                datetime.date(2030, 10, 15),
                datetime.date(2030, 10, 22),
                90,
                300,
                100,
                "リーディングに重点をおいてタスク生成したい",
            ),
        )

    def test_goal_with_space_goal_name(self):
        with self.assertRaises(IntegrityError):
            self._goal(goal_name=" ")
    
    def test_goal_with_zero_goal_name(self):
        with self.assertRaises(IntegrityError):
            self._goal(goal_name="")
    
    def test_goal_name_trim(self):
        goal = self._goal(goal_name="  TOEIC800点取得  ")
        self.assertEqual(goal.goal_name, "TOEIC800点取得")

    def test_goal_name_remove_fullwidth_space(self):
        goal = self._goal(goal_name="　TOEIC800点取得　")
        self.assertEqual(goal.goal_name, "TOEIC800点取得")

    def test_status_against_goal_trim(self):
        goal = self._goal(status_against_goal="  TOEIC模擬テストで400点を取得  ")
        self.assertEqual(goal.status_against_goal, "TOEIC模擬テストで400点を取得")

    def test_status_against_goal_remove_fullwidth_space(self):
        goal = self._goal(status_against_goal="　TOEIC模擬テストで400点を取得　")
        self.assertEqual(goal.status_against_goal, "TOEIC模擬テストで400点を取得")

    def test_goal_name_none(self):
        with self.assertRaises(ValueError):
            self._goal(goal_name=None)

    def test_status_against_goal_none(self):
        with self.assertRaises(ValueError):
            self._goal(status_against_goal=None)

    def test_start_day_not_date_type(self):
        with self.assertRaises(TypeError):
            self._goal(start_day="2030-10-15")

    def test_target_day_not_date_type(self):
        with self.assertRaises(TypeError):
            self._goal(target_day="2030-10-22")

    def test_goal_with_invalid_status(self):
        with self.assertRaises(ValueError):
            self._goal(status="作業中")

    def test_goal_with_valid_status(self):
        goal = self._goal(status="達成")
        self.assertEqual(goal.status, GoalsStatusEnum.Achieved.value)
    
    def test_default_status_enum_is_applied(self):
        goal = self._goal()
        self.assertEqual(goal.status, GoalsStatusEnum.Unachieved.value)
