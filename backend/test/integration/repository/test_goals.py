import datetime

from backend.models.models import Goals, GoalsStatusEnum, Users
from backend.repository.repository import (
    AchievedStatusImmutable,
    GoalRepository,
    StatusUnchangedError,
    UserRepository,
)
from backend.test.integration.test_base import TestBase
from sqlalchemy.exc import DataError, IntegrityError


class TestGoalRepository(TestBase):
    def setUp(self):
        super(TestGoalRepository, self).setUp()
        self.goal_repository = GoalRepository()
        user_repository = UserRepository()
        self.user = user_repository.register_user(
            self.db,
            Users(
                username="Aiueo",
                hashed_password="abcd",
                email="abcde@example.com",
            ),
            commit=True,
        )

    def _goal(self, **kwargs):
        defaults = dict(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=1140,
            task_creation_rule="リーディングに重点をおいてタスク生成したい",
        )
        defaults.update(kwargs)
        return Goals(**defaults)

    def _register_goal(self, **kwargs):
        goal_data = self._goal(**kwargs)
        return self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def _register_user(self, username: str, email: str):
        return UserRepository().register_user(
            self.db,
            Users(
                username=username,
                hashed_password="abcd",
                email=email,
            ),
            commit=True,
        )

    def test_delete_goal_from_db(self):
        goal = self._register_goal()
        self.goal_repository.delete_goal_from_db(self.db, goal)
        result = self.db.query(Goals).filter_by(goal_id=goal.goal_id).first()
        self.assertIsNone(result, "達成目標はデータベースから消去されていません")

    def test_update_goal_status_from_db(self):
        registered_goal = self._register_goal()
        self.goal_repository.update_goal_status_from_db(
            self.db,
            registered_goal.goal_id,
            GoalsStatusEnum.Achieved,
            commit=True,
        )
        self.assertEqual(registered_goal.status, GoalsStatusEnum.Achieved.value)

    def test_update_goal_status_from_db_achieved_immutable(self):
        registered_goal = self._register_goal(status=GoalsStatusEnum.Achieved.value)
        with self.assertRaises(AchievedStatusImmutable):
            self.goal_repository.update_goal_status_from_db(
                self.db,
                registered_goal.goal_id,
                GoalsStatusEnum.Unachieved,
                commit=True,
            )

    def test_update_goal_status_from_db_unchanged_raises(self):
        registered_goal = self._register_goal(status=GoalsStatusEnum.Unachieved.value)
        with self.assertRaises(StatusUnchangedError):
            self.goal_repository.update_goal_status_from_db(
                self.db,
                registered_goal.goal_id,
                GoalsStatusEnum.Unachieved,
                commit=True,
            )

    def test_search_goal_by_user_id_returns_only_unachieved(self):
        unachieved_goal = self._register_goal()
        self.db.add(self._goal(status=GoalsStatusEnum.Achieved.value))

        other_user = self._register_user(
            username="Kakikukeko",
            email="kakikukeko@example.com",
        )
        self.db.add(
            self._goal(
                goal_name="英検準1級取得",
                user_id=other_user.user_id,
                start_day=datetime.date(2030, 11, 1),
                target_day=datetime.date(2030, 11, 30),
                status_against_goal="英検模擬テストで60%",
                weekday_available_time=60,
                weekends_available_time=180,
                total_estimated_time=800,
                task_creation_rule="単語学習を優先したい",
            )
        )
        self.db.commit()

        goals = self.goal_repository.search_goal_by_user_id(self.db, self.user.user_id)

        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0].goal_id, unachieved_goal.goal_id)
        self.assertEqual(goals[0].status, GoalsStatusEnum.Unachieved.value)

    def test_search_goal_by_user_id_returns_empty_when_no_goal(self):
        other_user = self._register_user(
            username="Sasisuseso",
            email="sasisuseso@example.com",
        )

        goals = self.goal_repository.search_goal_by_user_id(self.db, other_user.user_id)

        self.assertEqual(goals, [])

    def test_fetch_goal_by_id_from_db_returns_goal(self):
        registered_goal = self._register_goal()

        goal = self.goal_repository.fetch_goal_by_id_from_db(
            self.db, registered_goal.goal_id
        )

        self.assertIsNotNone(goal)
        self.assertEqual(goal.goal_id, registered_goal.goal_id)

    def test_fetch_goal_by_id_from_db_returns_none_when_not_found(self):
        goal = self.goal_repository.fetch_goal_by_id_from_db(self.db, 999999)

        self.assertIsNone(goal)


class GoalsModelConstraintTest(TestBase):
    def setUp(self):
        super(GoalsModelConstraintTest, self).setUp()
        self.goal_repository = GoalRepository()
        self.user_data = Users(
            username="Aiueo",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        user_repository = UserRepository()
        self.user = user_repository.register_user(self.db, self.user_data, commit=True)

    def _goal(self, **kwargs):
        defaults = dict(
            goal_name="TOEIC800点取得",
            user_id=self.user.user_id,
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=1140,
            task_creation_rule="リーディングに重点をおいてタスク生成したい",
        )
        defaults.update(kwargs)
        return Goals(**defaults)

    def test_create_goal_with_start_day_before_target_day(self):
        goal_data = self._goal()
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.start_day, goal_data.start_day)
        self.assertEqual(goal.target_day, goal_data.target_day)

    def test_create_goal_with_start_day_equal_target_day(self):
        goal_data = self._goal(
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 15),
        )
        self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_start_day_after_target_day(self):
        goal_data = self._goal(
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 14),
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_start_day_before_today(self):
        goal_data = self._goal(
            start_day=datetime.date(2026, 4, 17), target_day=datetime.date(2030, 10, 22)
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_target_day_before_today(self):
        goal_data = self._goal(
            start_day=datetime.date(2030, 10, 15), target_day=datetime.date(2026, 4, 17)
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_datetime_start_day(self):
        goal_data = self._goal(
            start_day=datetime.datetime(2030, 10, 15, 10, 0),
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.start_day, datetime.date(2030, 10, 15))

    def test_create_goal_with_datetime_target_day(self):
        goal_data = self._goal(
            target_day=datetime.datetime(2030, 10, 22, 10, 0),
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.target_day, datetime.date(2030, 10, 22))

    def test_create_goal_with_0_status_against_goal(self):
        with self.assertRaises(ValueError):
            self._goal(status_against_goal="")

    def test_create_goal_with_1_status_against_goal(self):
        goal_data = self._goal(status_against_goal="あ")
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.status_against_goal, goal_data.status_against_goal)

    def test_create_goal_with_negative_weekday_available_time(self):
        goal_data = self._goal(
            weekday_available_time=-90,
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_invalid_weekday_available_time_before_lower_boundary(
        self,
    ):
        goal_data = self._goal(
            weekday_available_time=0,
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_create_goal_with_weekday_available_time_lower_boundary(self):
        goal_data = self._goal(
            weekday_available_time=1,
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_time, goal_data.weekday_available_time)

    def test_goal_with_weekday_available_time_before_upper_boundary(self):
        goal_data = self._goal(weekday_available_time=719)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_time, goal_data.weekday_available_time)

    def test_goal_with_weekday_available_time_upper_boundary(self):
        goal_data = self._goal(weekday_available_time=720)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.weekday_available_time, goal_data.weekday_available_time)

    def test_goal_with_invalid_weekday_available_time_after_upper_boundary(self):
        goal_data = self._goal(
            weekday_available_time=721,
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_negative_weekends_available_time(self):
        goal_data = self._goal(
            weekends_available_time=-300,
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_invalid_weekends_available_time_before_lower_boundary(self):
        goal_data = self._goal(
            weekends_available_time=0,
        )
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_weekends_available_time_lower_boundary(self):
        goal_data = self._goal(
            weekends_available_time=1,
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(
            goal.weekends_available_time, goal_data.weekends_available_time
        )

    def test_goal_with_weekends_available_time_before_upper_boundary(self):
        goal_data = self._goal(weekends_available_time=719)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(
            goal.weekends_available_time, goal_data.weekends_available_time
        )

    def test_goal_with_weekends_available_time_upper_boundary(self):
        goal_data = self._goal(weekends_available_time=720)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(
            goal.weekends_available_time, goal_data.weekends_available_time
        )

    def test_goal_with_invalid_weekends_available_time_after_upper_boundary(self):
        goal_data = self._goal(weekends_available_time=721)
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_negative_total_estimated_time_available_hours(self):
        goal_data = self._goal(total_estimated_time=-1140)
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_invalid_total_estimated_time_before_lower_boundary(self):
        goal_data = self._goal(total_estimated_time=0)
        with self.assertRaises(IntegrityError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_total_estimated_time_lower_boundary(self):
        goal_data = self._goal(total_estimated_time=1)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.total_estimated_time, goal_data.total_estimated_time)

    def test_goal_with_0_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule="")
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_1_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule="あ")
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_799_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule="あ" * 799)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_800_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule="あ" * 800)
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_801_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule="あ" * 801)
        with self.assertRaises(DataError):
            self.goal_repository.register_goal(self.db, goal_data, commit=True)

    def test_goal_with_space_task_creation_rule(self):
        goal_data = self._goal(task_creation_rule=" ")
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_none_task_creation_rule(self):
        goal_data = self._goal(
            weekday_available_time=90,
            weekends_available_time=300,
            total_estimated_time=1140,
            task_creation_rule=" ",
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_goal_with_none_task_creation_rule(self):
        goal_data = self._goal(
            task_creation_rule=None,
        )
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        self.assertEqual(goal.task_creation_rule, goal_data.task_creation_rule)

    def test_default_created_at_applied(self):
        goal_data = self._goal()
        goal = self.goal_repository.register_goal(self.db, goal_data, commit=True)
        now = datetime.datetime.now(datetime.timezone.utc)
        self.assertTrue(abs((now - goal.created_at).total_seconds()) < 5)
