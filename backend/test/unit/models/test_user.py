from unittest import TestCase
from backend.models.models import Users


class TestUser(TestCase):
    def _user(self, **kwargs):
        defaults = dict(
            username="sasa1231",
            hashed_password="abcd",
            email="abcde@example.com",
        )
        defaults.update(kwargs)
        return Users(**defaults)

    def test_user_sets_all_fields_correctly(self):
        user = self._user(user_points=100)
        self.assertEqual(
            (user.username, user.hashed_password, user.email, user.user_points),
            ("sasa1231", "abcd", "abcde@example.com", 100),
        )

    def test_user_with_1_username(self):
        user_data = self._user(username="あ")
        self.assertEqual(user_data.username, "あ")

    def test_user_with_blank_username(self):
        with self.assertRaises(ValueError):
            self._user(username="   ")

    def test_username_trim(self):
        user = self._user(username="  sasa1231  ")
        self.assertEqual(user.username, "sasa1231")

    def test_username_remove_fullwidth_space(self):
        user = self._user(username="　sasa　")
        self.assertEqual(user.username, "sasa")

    def test_username_none_raises_value_error(self):
        with self.assertRaises(ValueError):
            self._user(username=None)

    def test_user_with_empty_username_raises_value_error(self):
        with self.assertRaises(ValueError):
            self._user(username="")

    def test_user_points_integer(self):
        user = self._user(user_points=0)
        self.assertEqual(user.user_points, 0)

    def test_user_points_decimal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self._user(user_points=1.5)

    def test_invalid_user_rank_raises_value_error(self):
        with self.assertRaises(ValueError):
            self._user(username="user", email="test@example.com", user_rank="最強")
