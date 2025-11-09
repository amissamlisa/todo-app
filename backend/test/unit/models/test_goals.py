from unittest import TestCase
import datetime
from backend.models.models import Goals


class GoalsTest(TestCase):
    # 初期化時に値が正しく設定された場合
    def test_create_goal(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 1140

        self.assertEqual(goal.goal_name, "TOEIC800点取得",
                         "goal_nameの値が一致しません")
        self.assertEqual(goal.start_day, datetime.date(2030, 10, 15),
                         "goal_start_dayの値が一致しません")
        self.assertEqual(goal.target_day, datetime.date(2030, 10, 22),
                         "goal_target_dayの値が一致しません")
        self.assertEqual(goal.weekday_available_time, 90,
                         "weekday_available_timeの値が一致しません")
        self.assertEqual(goal.weekends_available_time, 300,
                         "weekends_available_timeの値が一致しません")
        self.assertEqual(result, expected_result,
                         "total_estimated_timeの値が一致しません")
        self.assertEqual(goal.task_creation_rule, "リーディングに重点をおいてタスク生成したい",
                         "task_creation_ruleの値が一致しません")

    # 目標タスク開始日と終了日が同じ場合
    def test_calculate_total_estimated_time_same_day(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 15),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=60,
            weekends_available_time=90,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 60

        self.assertEqual(result, expected_result)

    # 平日のみ
    def test_calculate_total_estimated_time_weekday_only(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 18),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 360

        self.assertEqual(result, expected_result)

    # 土日のみの場合
    def test_calculate_total_estimated_time_weekends_only(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 19),
            target_day=datetime.date(2030, 10, 20),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 600

        self.assertEqual(result, expected_result)

    # タスク開始日が終了日よりも遅い場合
    def test_calculate_total_estimated_time_invalid_value(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 18),
            target_day=datetime.date(2030, 10, 1),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 0

        self.assertEqual(result, expected_result)

    # 祝日が含まれる場合
    def test_calculate_total_estimated_time_includes_holiday(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 11),
            target_day=datetime.date(2030, 10, 14),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 990

        self.assertEqual(result, expected_result)

    # 平日から週末に切り替わる場合
    def test_calculate_total_estimated_time_from_weekday_to_weekend(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 18),
            target_day=datetime.date(2030, 10, 19),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 390

        self.assertEqual(result, expected_result)

    # 年をまたぐ場合
    def test_calculate_total_estimated_time_year_cross(self):
        goal = Goals(
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 12, 31),
            target_day=datetime.date(2031, 1, 1),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=0,
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        result = goal.calculate_total_estimated_time()
        expected_result = 390

        self.assertEqual(result, expected_result)
