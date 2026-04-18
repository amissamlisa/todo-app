from sqlalchemy.exc import IntegrityError

from backend.models.models import Users
from backend.repository.repository import EmailAlreadyRegistered, UserRepository
from backend.test.integration.test_base import TestBase


class TestUserRepository(TestBase):
    def setUp(self):
        super(TestUserRepository, self).setUp()
        self.user_repository = UserRepository()

    def _user(self, **kwargs):
        defaults = {
            "username": "user1",
            "hashed_password": "abcd",
            "email": "abcde@example.com",
        }
        defaults.update(kwargs)
        return Users(**defaults)

    def _register_user(self, **kwargs):
        user_data = self._user(**kwargs)
        return self.user_repository.register_user(self.db, user_data, commit=True)

    def test_user_with_the_same_email(self):
        self._register_user()
        user2_data = self._user(username="user2")
        with self.assertRaises(EmailAlreadyRegistered):
            self.user_repository.register_user(self.db, user2_data, commit=True)

    def test_user_with_none_hashed_password(self):
        user_data = self._user(hashed_password=None)
        with self.assertRaises(IntegrityError):
            self.user_repository.register_user(self.db, user_data, commit=True)

    def test_user_with_none_email(self):
        user_data = self._user(email=None)
        with self.assertRaises(IntegrityError):
            self.user_repository.register_user(self.db, user_data, commit=True)

    def test_user_with_negative_user_points(self):
        user_data = self._user(user_points=-1)
        with self.assertRaises(IntegrityError):
            self.user_repository.register_user(self.db, user_data, commit=True)

    def test_user_with_1_user_points(self):
        user_data = self._register_user(user_points=1)
        self.assertEqual(user_data.user_points, 1)

    def test_user_with_100_user_points(self):
        user_data = self._register_user(user_points=100)
        self.assertEqual(user_data.user_points, 100)

    def test_find_user_by_email(self):
        user = self._register_user()

        found_user = self.user_repository.find_user_by_email(
            self.db, "abcde@example.com"
        )

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.user_id, user.user_id)

    def test_find_user_by_email_not_found(self):
        found_user = self.user_repository.find_user_by_email(
            self.db, "notfound@example.com"
        )
        self.assertIsNone(found_user)

    def test_find_user_by_user_id(self):
        user = self._register_user()

        found_user = self.user_repository.find_user_by_user_id(self.db, user.user_id)

        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, user.email)

    def test_find_user_by_user_id_not_found(self):
        found_user = self.user_repository.find_user_by_user_id(self.db, 99999)
        self.assertIsNone(found_user)

    def test_update_user_points(self):
        user = self._register_user(user_points=1)

        updated_user = self.user_repository.update_user_points_from_db(
            self.db,
            user.user_id,
            200,
            commit=True,
        )

        self.assertEqual(updated_user.user_points, 200)

    def test_update_user_points_returns_none_when_user_not_found(self):
        updated_user = self.user_repository.update_user_points_from_db(
            self.db,
            99999,
            200,
            commit=True,
        )

        self.assertIsNone(updated_user)

    def test_update_user_rank(self):
        user = self._register_user(user_rank="雫")

        updated_user = self.user_repository.update_user_rank_from_db(
            self.db,
            user.user_id,
            "霧",
            commit=True,
        )

        self.assertEqual(updated_user.user_rank, "霧")

    def test_update_user_rank_returns_none_when_user_not_found(self):
        updated_user = self.user_repository.update_user_rank_from_db(
            self.db,
            99999,
            "霧",
            commit=True,
        )

        self.assertIsNone(updated_user)

    def test_update_user(self):
        user_data = self._user(user_points=100, user_rank="雲")

        updated_user_data = Users(
            username="user2",
            hashed_password="cdbe",
            email="efgd@example.com",
        )

        user = self.user_repository.register_user(self.db, user_data, commit=True)
        updated_user = self.user_repository.update_user_from_db(
            self.db, user.user_id, updated_user_data, commit=True
        )
        self.assertEqual(
            (user.username, user.hashed_password, user.email, user.user_points),
            (
                updated_user.username,
                updated_user.hashed_password,
                updated_user.email,
                updated_user.user_points,
            ),
        )
        self.assertEqual(updated_user.user_rank, "雲")

    def test_update_user_not_found(self):
        updated_user_data = Users(
            username="x",
            hashed_password="x",
            email="x@test.com",
        )
        with self.assertRaises(AttributeError):
            self.user_repository.update_user_from_db(
                self.db,
                99999,
                updated_user_data,
                commit=True,
            )
