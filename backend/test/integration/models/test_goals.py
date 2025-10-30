import datetime
from backend.models.models import Goals, GoalsStatusEnum, Users
from backend.repository.repository import GoalRepository, UserRepository
from backend.test.integration.models.test_base import TestBase
from decimal import Decimal
from sqlalchemy.exc import DataError, IntegrityError, StatementError


class GoalsTest(TestBase):
    def setUp(self):
        super(GoalsTest, self).setUp()
        self.goal_repository = GoalRepository()
        self.user_data = Users(
            username="Aiueo",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        user_repository = UserRepository()
        self.user = user_repository.register_user(self.db, self.user_data, commit=True)

    def test_create_goal_with_0_goal_name(self):
        goal_data = Goals(
            goal_name="",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_1_goal_name(self):
        goal_data = Goals(
            goal_name="あ",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.goal_name, goal_data.goal_name)

    def test_create_goal_with_50_goal_name(self):
        goal_data = Goals(
            goal_name="あ" * 50,
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.goal_name, goal_data.goal_name)

    def test_create_goal_with_99_goal_name(self):
        goal_data = Goals(
            goal_name="あ" * 99,
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.goal_name, goal_data.goal_name)

    def test_create_goal_with_100_goal_name(self):
        goal_data = Goals(
            goal_name="あいうえおかきくけこ" * 10,
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.goal_name, goal_data.goal_name)

    def test_create_goal_with_101_goal_name(self):
        goal_data = Goals(
            goal_name="あ" * 101,
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_300_goal_name(self):
        goal_data = Goals(
            goal_name="あ" * 300,
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_space_goal_name(self):
        goal_data = Goals(
            goal_name=" ",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_none_goal_name(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name=None,
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_default_status_enum_is_applied(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status, GoalsStatusEnum.Unachieved)

    def test_valid_status_enum_is_applied(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            status=GoalsStatusEnum.Achieved,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status, goal_data.status)

    def test_invalid_status_enum_is_applied(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            status="進行中",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(StatementError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_start_day_before_target_day(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.start_day, goal_data.start_day)
        self.assertEqual(goal.target_day, goal_data.target_day)

    def test_create_goal_with_start_day_equal_target_day(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 15),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal_repository = GoalRepository()
        goal = goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.start_day, goal_data.start_day)
        self.assertEqual(goal.target_day, goal_data.target_day)

    def test_create_goal_with_start_day_after_target_day(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 14),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_start_day_before_now(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2025, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_target_day_before_now(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2025, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_none_start_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=None,
                target_day=datetime.date(2025, 10, 14),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_none_target_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=None,
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_string_start_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day="2030/10/10",
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_string_target_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day="2030/10/22",
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_invalid_str_start_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day="TOEIC800点取得",
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_invalid_str_target_day(self):
        with self.assertRaises(TypeError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day="TOEIC800点取得",
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_datetime_start_day(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.datetime(2030, 10, 15, 10, 0),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.start_day, datetime.date(2030, 10, 15))

    def test_create_goal_with_datetime_target_day(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.datetime(2030, 10, 22, 10, 0),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.target_day, datetime.date(2030, 10, 22))

    def test_create_goal_with_0_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_1_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status_against_goal, goal_data.status_against_goal)

    def test_create_goal_with_80_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ" * 80,
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status_against_goal, goal_data.status_against_goal)

    def test_create_goal_with_199_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ" * 199,
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status_against_goal, goal_data.status_against_goal)

    def test_create_goal_with_200_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ" * 200,
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status_against_goal, goal_data.status_against_goal)

    def test_create_goal_with_201_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ" * 201,
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_500_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="あ" * 500,
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_none_status_against_goal(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal=None,
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_space_status_against_goal(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal=" ",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_negative_weekday_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("-15.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_weekday_available_hours_before_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("0.0"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_weekday_available_hours_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("0.1"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_weekday_available_hours_after_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("0.2"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_valid_weekday_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("100.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_weekday_available_hours_before_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("999.8"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_weekday_available_hours_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("999.9"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_invalid_weekday_available_hours_after_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1000.0"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_weekday_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("4000.1"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_weekday_available_hours_exceeds_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("99.99"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_weekday_available_hours_with_4_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("99.9999"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_weekday_available_hours_valid_scale(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("99.9"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_weekday_available_hours_integer_only(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("99"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_hours, goal_data.weekday_available_hours)

    def test_create_goal_with_negative_weekends_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("-15.1"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_weekends_available_hours_before_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("0.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_weekends_available_hours_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("0.1"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_weekends_available_hours_after_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("0.2"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_valid_weekends_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("100.5"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_weekends_available_hours_before_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("999.8"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_weekends_available_hours_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("999.9"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_invalid_weekends_available_hours_after_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("1000.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_weekends_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("4000.1"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_weekends_available_hours_exceeds_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("99.99"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_weekends_available_hours_with_4_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("99.9999"),
                total_estimated_time=Decimal("19.0"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_weekends_available_hours_valid_scale(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("99.9"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_weekends_available_hours_integer_only(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("99"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekends_available_hours, goal_data.weekends_available_hours)

    def test_create_goal_with_negative_total_estimated_time_available_hours(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("-15.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_total_estimated_time_before_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("0.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_total_estimated_time_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("0.1"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_total_estimated_time_after_lower_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("0.2"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_valid_total_estimated_time(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("100.5"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_total_estimated_time_before_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("999.8"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_total_estimated_time_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("999.9"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_invalid_total_estimated_time_after_upper_boundary(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("1000.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_total_estimated_time(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("4000.1"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_total_estimated_time_exceeds_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("99.99"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_total_estimated_time_with_4_scale(self):
        with self.assertRaises(ValueError):
            Goals(
                goal_name="TOEIC800点取得",
                user_id=self.user.user_id,
                start_day=datetime.date(2030, 10, 15),
                target_day=datetime.date(2030, 10, 22),
                status_against_goal="TOEIC模擬テストで400点を取得",
                weekday_available_hours=Decimal("1.5"),
                weekends_available_hours=Decimal("5.0"),
                total_estimated_time=Decimal("99.9999"),
                task_creation_rule="リーディングに重点をおいてタスク生成したい"
            )

    def test_create_goal_with_total_estimated_times_valid_scale(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("99.9"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_total_estimated_time_integer_only(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("99"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_create_goal_with_0_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule=""
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_1_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_400_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ" * 400,
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_799_goal_name(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ" * 799
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_800_goal_name(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ" * 800
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_801_goal_name(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ" * 801
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_1000_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="あ" * 1000
        )
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_space_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule=" "
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_create_goal_with_none_task_creation_rule(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule=None
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_default_created_at_applied(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        now = datetime.datetime.now()
        self.assertTrue(abs((now - goal.created_at).total_seconds()) < 5)

    def test_delete_goal_from_db(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.goal_repository.delete_goal_from_db(self.db, goal)
        result = self.db.query(Goals).filter_by(goal_id=goal.goal_id).first()
        self.assertIsNone(result, "達成目標はデータベースから消去されていません")

    def test_update_goal_status_from_db(self):
        goal_data = Goals(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        registered_goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.goal_repository.update_goal_status_from_db(self.db, registered_goal.goal_id, commit=True)
        self.assertEqual(registered_goal.status, GoalsStatusEnum.Achieved)
