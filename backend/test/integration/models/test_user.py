import datetime
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from backend.models.models import Goals, Users
from backend.repository.repository import GoalRepository, GoalTaskRepository, UserRepository
from backend.test.integration.models.test_base import TestBase


class TestUser(TestBase):
    def setUp(self):
        super(TestUser, self).setUp()
        self.goal_user_repository = UserRepository()

    def test_create_user_with_0_username(self):
        user_data = Users(
            username="",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        with self.assertRaises(IntegrityError):
            self.goal_user_repository.register_user(self.db, user_data, commit=True)

    def test_create_user_with_2_username(self):
        user_data = Users(
            username="あ",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        with self.assertRaises(IntegrityError):
            self.goal_user_repository.register_user(self.db, user_data, commit=True)

    def test_create_user_with_3_username(self):
        user_data = Users(
            username="あ" * 3,
            hashed_password="abcd",
            email="abcde@example.com",
        )
        user = self.goal_user_repository.register_user(self.db, user_data, commit=True)
        self.assertEqual(user.username, user_data.username)

    def test_create_user_with_50_username(self):
        user_data = Users(
            username="あ" * 50,
            hashed_password="abcd",
            email="abcde@example.com",
        )
        user = self.goal_user_repository.register_user(self.db, user_data, commit=True)
        self.assertEqual(user.username, user_data.username)

    def test_create_user_with_space_username(self):
        user_data = Users(
            username=" ",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        with self.assertRaises(IntegrityError):
            self.goal_user_repository.register_user(self.db, user_data, commit=True)

    def test_create_user_with_none_username(self):
        with self.assertRaises(ValueError):
            Users(
                username=None,
                hashed_password="abcd",
                email="abcde@example.com",
            )

    def test_create_user_with_ths_same_email(self):
        user1_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        self.goal_user_repository.register_user(self.db, user1_data, commit=True)
        user2_data = Users(
            username="user2",
            hashed_password="abcd",
            email="abcde@example.com"
        )
        with self.assertRaises(IntegrityError):
            self.goal_user_repository.register_user(self.db, user2_data, commit=True)

    def test_default_user_points_is_applied(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        self.goal_user_repository.register_user(self.db, user_data, commit=True)

        self.assertEqual(user_data.user_points, 0)

    def test_default_user_points_are_applied(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        self.goal_user_repository.register_user(self.db, user_data, commit=True)

        self.assertEqual(user_data.user_points, 0)

    def test_create_user_with_negative_user_points(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=-1
        )
        with self.assertRaises(IntegrityError):
            self.goal_user_repository.register_user(self.db, user_data, commit=True)

    def test_create_user_with_1_user_points(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=1
        )
        self.goal_user_repository.register_user(self.db, user_data, commit=True)
        self.assertEqual(user_data.user_points, 1)

    def test_create_user_with_100_user_points(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=100
        )
        self.goal_user_repository.register_user(self.db, user_data, commit=True)
        self.assertEqual(user_data.user_points, 100)

    def test_create_user_with_decimal_user_points(self):
        with self.assertRaises(ValueError):
            Users(
                username="user1",
                hashed_password="abcd",
                email="abcde@example.com",
                user_points=100.5
            )

    def test_default_created_at_is_applied(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=100
        )
        user = self.goal_user_repository.register_user(self.db, user_data, commit=True)
        now = datetime.datetime.now()
        self.assertTrue(abs((now - user.created_at).total_seconds()) < 5)

    def test_update_user(self):
        user_data = Users(
            username="user1",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=100
        )

        updated_user_data = Users(
            username="user2",
            hashed_password="cdbe",
            email="efgd@example.com",
        )

        user = self.goal_user_repository.register_user(self.db, user_data, commit=True)
        updated_user = self.goal_user_repository.update_user_from_db(self.db, user.user_id, updated_user_data, commit=True)
        self.assertEqual(user.username, updated_user.username)
        self.assertEqual(user.hashed_password, updated_user.hashed_password)
        self.assertEqual(user.email, updated_user.email)
        self.assertEqual(user.user_points, updated_user.user_points)

