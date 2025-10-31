import datetime
from decimal import Decimal

from sqlalchemy.exc import IntegrityError, DataError, StatementError
from backend.models.models import GoalsTasks, Goals, GoalsTasksStatusEnum, Users
from backend.repository.repository import GoalTaskRepository, GoalRepository, UserRepository
from backend.test.integration.models.test_base import TestBase


class TestGoalTasks(TestBase):
    def setUp(self):
        super(TestGoalTasks, self).setUp()
        user_data = Users(
            username="abced",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        self.user = UserRepository().register_user(self.db, user_data, commit=True)
        self.goal_data = Goals(
            user_id=self.user.user_id,
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_hours=Decimal("1.5"),
            weekends_available_hours=Decimal("5.0"),
            total_estimated_time=Decimal("19.0"),
            task_creation_rule="リーディングに重点をおいてタスク生成したい"
        )
        goal_repository = GoalRepository()
        self.goal = goal_repository.register_goal(self.db, self.goal_data, commit=True)
        self.goal_task_repository = GoalTaskRepository()

    def test_create_goal_task_with_0_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(IntegrityError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_1_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_name, goal_task_data.goal_task_name)

    def test_create_goal_task_with_20_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ" * 20,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_name, goal_task_data.goal_task_name)

    def test_create_goal_task_with_49_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ" * 49,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_name, goal_task_data.goal_task_name)

    def test_create_goal_task_with_50_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ" * 50,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_name, goal_task_data.goal_task_name)

    def test_create_goal_task_with_51_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ" * 51,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(DataError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_100_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="あ" * 100,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(DataError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_space_goal_task_name(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="  ",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(IntegrityError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_none_goal_task_name(self):
        with self.assertRaises(ValueError):
            goal_task_data = GoalsTasks(
                goal_id=self.goal.goal_id,
                goal_task_name=None,
                deadline=datetime.date(2030, 10, 15),
                estimated_time=Decimal("3.0"),
            )
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_default_goal_task_status_is_applied(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_status, GoalsTasksStatusEnum.Todo)

    def test_goal_task_in_progress_status_enum_is_applied(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            goal_task_status=GoalsTasksStatusEnum.InProgress,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_status, goal_task_data.goal_task_status)

    def test_goal_task_completed_status_enum_is_applied(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            goal_task_status=GoalsTasksStatusEnum.Completed,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.goal_task_status, goal_task.goal_task_status)

    def test_invalid_goal_task_enum_is_applied(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            goal_task_status="完了",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(StatementError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_deadline_before_now(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2025, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        with self.assertRaises(IntegrityError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_string_deadline(self):
        with self.assertRaises(TypeError):
            goal_task_data = GoalsTasks(
                goal_id=self.goal.goal_id,
                goal_task_name="英単語帳を暗記",
                deadline="2030/10/22",
                estimated_time=Decimal("3.0"),
            )
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_invalid_deadline(self):
        with self.assertRaises(TypeError):
            goal_task_data = GoalsTasks(
                goal_id=self.goal.goal_id,
                goal_task_name="英単語帳を暗記",
                deadline="TOEIC800点取得",
                estimated_time=Decimal("3.0"),
            )
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_datetime_deadline(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.datetime(2030, 10, 15, 10, 0),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.deadline, datetime.date(2030, 10, 15))

    def test_create_goal_task_with_valid_deadline(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.deadline, goal_task_data.deadline)

    def test_create_goal_task_with_negative_estimated_time(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("-3.0"),
        )
        with self.assertRaises(IntegrityError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_invalid_estimated_time_before_lower_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("0.0"),
        )
        with self.assertRaises(IntegrityError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_estimated_time_lower_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("0.1"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_estimated_time_after_lower_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("0.2"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_valid_estimated_time(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_estimated_time_before_upper_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("999.8"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_estimated_time_upper_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("999.9"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_estimated_time_after_upper_boundary(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("1000.0"),
        )
        with self.assertRaises(DataError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_invalid_estimated_time(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3000.5"),
        )
        with self.assertRaises(DataError):
            self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)

    def test_create_goal_task_with_estimated_time_exceeds_scale(self):
        with self.assertRaises(ValueError):
            GoalsTasks(
                goal_id=self.goal.goal_id,
                goal_task_name="英単語帳を暗記",
                deadline=datetime.date(2030, 10, 15),
                estimated_time=Decimal("99.55"),
            )

    def test_create_goal_task_with_estimated_time_with_4_scale(self):
        with self.assertRaises(ValueError):
            GoalsTasks(
                goal_id=self.goal.goal_id,
                goal_task_name="英単語帳を暗記",
                deadline=datetime.date(2030, 10, 15),
                estimated_time=Decimal("99.5555"),
            )

    def test_create_goal_task_with_estimated_times_valid_scale(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("99.9"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_create_goal_task_with_estimated_time_integer_only(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("99"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.assertEqual(goal_task.estimated_time, goal_task_data.estimated_time)

    def test_default_created_at_applied(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )
        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        now = datetime.datetime.now()
        self.assertTrue(abs((now - goal_task.created_at).total_seconds()) < 5)

    def test_delete_goal_task_from_db(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )

        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.goal_task_repository.delete_goal_task_from_db(self.db, goal_task)
        result = self.db.query(GoalsTasks).filter_by(goal_task_id=goal_task.goal_id).first()
        self.assertIsNone(result, "達成目標タスクはデータベースから消去されていません")

    def test_update_goal_task_status_to_completed_from_db(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )

        goal_task = self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        self.goal_task_repository.update_goal_task_stauts_from_db(self.db, goal_task_data.goal_task_id,
                                                                  GoalsTasksStatusEnum.Completed)
        self.assertEqual(goal_task.goal_task_status, GoalsTasksStatusEnum.Completed)

    def test_update_goal_task_status_to_same_goal_task_status_from_db(self):
        goal_task_data = GoalsTasks(
            goal_id=self.goal.goal_id,
            goal_task_status=GoalsTasksStatusEnum.InProgress,
            goal_task_name="英単語帳を暗記",
            deadline=datetime.date(2030, 10, 15),
            estimated_time=Decimal("3.0"),
        )

        self.goal_task_repository.register_goal_task(self.db, goal_task_data, commit=True)
        with self.assertRaises(ValueError):
            self.goal_task_repository.update_goal_task_stauts_from_db(self.db, goal_task_data.goal_task_id,
                                                                      GoalsTasksStatusEnum.InProgress)
