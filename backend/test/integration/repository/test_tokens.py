import datetime

from sqlalchemy.exc import DataError, IntegrityError

from backend.models.models import PasswordResetTokens, RefreshTokens, Users
from backend.repository.repository import (
    PasswordResetRepository,
    RefreshTokenRepository,
    UserRepository,
)
from backend.test.integration.test_base import TestBase


class RefreshTokenTest(TestBase):
    def setUp(self):
        super().setUp()
        user_data = Users(
            username="tokenuser", hashed_password="abcd", email="tokenuser@example.com"
        )
        self.user = UserRepository().register_user(self.db, user_data, commit=True)
        self.refresh_token_repository = RefreshTokenRepository()

    def _dt(self, year, month, day):
        return datetime.datetime(year, month, day, 12, 0, tzinfo=datetime.timezone.utc)

    def _refresh_token(self, **kwargs):
        defaults = {
            "user_id": self.user.user_id,
            "token_prefix": "abcdef",
            "hashed_token": "a" * 72,
            "expires_at": self._dt(2030, 10, 15),
        }
        defaults.update(kwargs)
        return RefreshTokens(**defaults)

    def test_register_refresh_token_success(self):
        refresh_token = self._refresh_token()

        created_token = self.refresh_token_repository.register_refresh_token(
            self.db, refresh_token, commit=True
        )

        self.assertEqual(created_token.user_id, self.user.user_id)
        self.assertEqual(created_token.token_prefix, "abcdef")
        self.assertIsNone(created_token.revoked_at)

    def test_register_refresh_token_with_duplicate_hashed_token(self):
        first_token = self._refresh_token()
        second_token = self._refresh_token(
            token_prefix="ghijkl", expires_at=self._dt(2030, 10, 16)
        )

        self.refresh_token_repository.register_refresh_token(
            self.db, first_token, commit=True
        )
        with self.assertRaises(IntegrityError):
            self.refresh_token_repository.register_refresh_token(
                self.db, second_token, commit=True
            )

    def test_register_refresh_token_with_none_user_id(self):
        refresh_token = self._refresh_token(user_id=None)

        with self.assertRaises(IntegrityError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_register_refresh_token_with_none_token_prefix(self):
        refresh_token = self._refresh_token(token_prefix=None)

        with self.assertRaises(IntegrityError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_register_refresh_token_with_token_prefix_too_long(self):
        refresh_token = self._refresh_token(token_prefix="abcdefg")

        with self.assertRaises(DataError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_register_refresh_token_with_none_hashed_token(self):
        refresh_token = self._refresh_token(hashed_token=None)

        with self.assertRaises(IntegrityError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_register_refresh_token_with_hashed_token_too_long(self):
        refresh_token = self._refresh_token(hashed_token="a" * 73)

        with self.assertRaises(DataError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_register_refresh_token_with_none_expires_at(self):
        refresh_token = self._refresh_token(expires_at=None)

        with self.assertRaises(IntegrityError):
            self.refresh_token_repository.register_refresh_token(
                self.db, refresh_token, commit=True
            )

    def test_revoke_refresh_token_success(self):
        refresh_token = self._refresh_token()
        created_token = self.refresh_token_repository.register_refresh_token(
            self.db, refresh_token, commit=True
        )

        revoked_token = self.refresh_token_repository.revoke_refresh_token(
            self.db, created_token.refresh_token_id, commit=True
        )

        self.assertIsNotNone(revoked_token.revoked_at)

    def test_revoke_all_user_tokens_success(self):
        first_token = self._refresh_token(token_prefix="first1", hashed_token="a" * 72)
        second_token = self._refresh_token(
            token_prefix="second",
            hashed_token="b" * 72,
            expires_at=self._dt(2030, 10, 16),
        )
        already_revoked_token = self._refresh_token(
            token_prefix="third3",
            hashed_token="c" * 72,
            expires_at=self._dt(2030, 10, 17),
            revoked_at=self._dt(2030, 10, 14),
        )

        self.refresh_token_repository.register_refresh_token(
            self.db, first_token, commit=True
        )
        self.refresh_token_repository.register_refresh_token(
            self.db, second_token, commit=True
        )
        self.refresh_token_repository.register_refresh_token(
            self.db, already_revoked_token, commit=True
        )

        revoked_count = self.refresh_token_repository.revoke_all_user_tokens(
            self.db, self.user.user_id, commit=True
        )

        refreshed_first_token = self.db.get(RefreshTokens, first_token.refresh_token_id)
        refreshed_second_token = self.db.get(
            RefreshTokens, second_token.refresh_token_id
        )
        refreshed_revoked_token = self.db.get(
            RefreshTokens, already_revoked_token.refresh_token_id
        )

        self.assertEqual(revoked_count, 2)
        self.assertIsNotNone(refreshed_first_token.revoked_at)
        self.assertIsNotNone(refreshed_second_token.revoked_at)
        self.assertEqual(
            refreshed_revoked_token.revoked_at,
            self._dt(2030, 10, 14),
        )

    def test_revoke_all_user_tokens_returns_zero_when_active_tokens_absent(self):
        revoked_count = self.refresh_token_repository.revoke_all_user_tokens(
            self.db, self.user.user_id, commit=True
        )

        self.assertEqual(revoked_count, 0)

    def test_delete_expired_refresh_tokens_deletes_only_expired(self):
        expired_token = self._refresh_token(
            token_prefix="old111",
            hashed_token="a" * 72,
            expires_at=self._dt(2020, 10, 15),
        )
        valid_token = self._refresh_token(
            token_prefix="new111",
            hashed_token="b" * 72,
            expires_at=self._dt(2030, 10, 15),
        )

        self.refresh_token_repository.register_refresh_token(
            self.db, expired_token, commit=True
        )
        self.refresh_token_repository.register_refresh_token(
            self.db, valid_token, commit=True
        )

        deleted_count = self.refresh_token_repository.delete_expired_refresh_tokens(
            self.db, now=self._dt(2025, 1, 1), commit=True
        )

        remaining_tokens = self.db.query(RefreshTokens).all()

        self.assertEqual(deleted_count, 1)
        self.assertEqual(len(remaining_tokens), 1)
        self.assertEqual(remaining_tokens[0].token_prefix, "new111")

    def test_delete_expired_refresh_tokens_returns_zero_when_none_expired(self):
        valid_token = self._refresh_token(
            token_prefix="valid1",
            hashed_token="a" * 72,
            expires_at=self._dt(2030, 10, 15),
        )
        self.refresh_token_repository.register_refresh_token(
            self.db, valid_token, commit=True
        )

        deleted_count = self.refresh_token_repository.delete_expired_refresh_tokens(
            self.db, now=self._dt(2025, 1, 1), commit=True
        )

        self.assertEqual(deleted_count, 0)


class PasswordResetTokenTest(TestBase):
    def setUp(self):
        super().setUp()
        user_data = Users(
            username="resetuser", hashed_password="abcd", email="resetuser@example.com"
        )
        self.user = UserRepository().register_user(self.db, user_data, commit=True)
        self.password_reset_repository = PasswordResetRepository()

    def _dt(self, year, month, day):
        return datetime.datetime(year, month, day, 12, 0, tzinfo=datetime.timezone.utc)

    def _password_reset_token(self, **kwargs):
        defaults = {
            "user_id": self.user.user_id,
            "token_prefix": "mnopqr",
            "hashed_token": "b" * 72,
            "expires_at": self._dt(2030, 10, 20),
        }
        defaults.update(kwargs)
        return PasswordResetTokens(**defaults)

    def test_register_password_reset_token_success(self):
        password_reset_token = self._password_reset_token()

        created_token = self.password_reset_repository.register_password_reset_token(
            self.db, password_reset_token, commit=True
        )

        self.assertEqual(created_token.user_id, self.user.user_id)
        self.assertEqual(created_token.token_prefix, "mnopqr")

    def test_register_password_reset_token_with_duplicate_hashed_token(self):
        first_token = self._password_reset_token()
        second_token = self._password_reset_token(
            token_prefix="stuvwx", expires_at=self._dt(2030, 10, 21)
        )

        self.password_reset_repository.register_password_reset_token(
            self.db, first_token, commit=True
        )
        with self.assertRaises(IntegrityError):
            self.password_reset_repository.register_password_reset_token(
                self.db, second_token, commit=True
            )

    def test_register_password_reset_token_with_none_user_id(self):
        password_reset_token = self._password_reset_token(user_id=None)

        with self.assertRaises(IntegrityError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_register_password_reset_token_with_none_token_prefix(self):
        password_reset_token = self._password_reset_token(token_prefix=None)

        with self.assertRaises(IntegrityError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_register_password_reset_token_with_token_prefix_too_long(self):
        password_reset_token = self._password_reset_token(token_prefix="mnopqrs")

        with self.assertRaises(DataError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_register_password_reset_token_with_none_hashed_token(self):
        password_reset_token = self._password_reset_token(hashed_token=None)

        with self.assertRaises(IntegrityError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_register_password_reset_token_with_hashed_token_too_long(self):
        password_reset_token = self._password_reset_token(hashed_token="b" * 73)

        with self.assertRaises(DataError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_register_password_reset_token_with_none_expires_at(self):
        password_reset_token = self._password_reset_token(expires_at=None)

        with self.assertRaises(IntegrityError):
            self.password_reset_repository.register_password_reset_token(
                self.db, password_reset_token, commit=True
            )

    def test_delete_password_reset_token_success(self):
        password_reset_token = self._password_reset_token()
        created_token = self.password_reset_repository.register_password_reset_token(
            self.db, password_reset_token, commit=True
        )

        self.password_reset_repository.delete_password_reset_token(
            self.db, created_token, commit=True
        )
        fetched_tokens = (
            self.password_reset_repository.get_password_refresh_token_by_prefix(
                self.db, "mnopqr"
            )
        )

        self.assertEqual(fetched_tokens, [])

    def test_get_password_refresh_token_by_prefix_returns_matching_tokens(self):
        first_token = self._password_reset_token()
        second_token = self._password_reset_token(
            hashed_token="c" * 72,
            expires_at=self._dt(2030, 10, 21),
        )
        other_prefix_token = self._password_reset_token(
            token_prefix="stuvwx",
            hashed_token="d" * 72,
            expires_at=self._dt(2030, 10, 22),
        )

        self.password_reset_repository.register_password_reset_token(
            self.db, first_token, commit=True
        )
        self.password_reset_repository.register_password_reset_token(
            self.db, second_token, commit=True
        )
        self.password_reset_repository.register_password_reset_token(
            self.db, other_prefix_token, commit=True
        )

        fetched_tokens = (
            self.password_reset_repository.get_password_refresh_token_by_prefix(
                self.db, "mnopqr"
            )
        )

        self.assertEqual(len(fetched_tokens), 2)
        self.assertTrue(all(token.token_prefix == "mnopqr" for token in fetched_tokens))

    def test_get_password_refresh_token_by_prefix_returns_empty_when_not_found(self):
        fetched_tokens = (
            self.password_reset_repository.get_password_refresh_token_by_prefix(
                self.db, "zzzzzz"
            )
        )

        self.assertEqual(fetched_tokens, [])

    def test_update_password_from_db(self):
        updated_user = self.password_reset_repository.update_password_from_db(
            self.db,
            self.user.user_id,
            "updated_password_hash",
            commit=True,
        )

        self.assertEqual(updated_user.hashed_password, "updated_password_hash")

    def test_update_password_from_db_not_found(self):
        with self.assertRaises(AttributeError):
            self.password_reset_repository.update_password_from_db(
                self.db,
                99999,
                "updated_password_hash",
                commit=True,
            )

    def test_delete_expired_password_reset_tokens_deletes_only_expired(self):
        expired_token = self._password_reset_token(
            token_prefix="oldpw1",
            hashed_token="b" * 72,
            expires_at=self._dt(2020, 10, 20),
        )
        valid_token = self._password_reset_token(
            token_prefix="newpw1",
            hashed_token="c" * 72,
            expires_at=self._dt(2030, 10, 20),
        )

        self.password_reset_repository.register_password_reset_token(
            self.db, expired_token, commit=True
        )
        self.password_reset_repository.register_password_reset_token(
            self.db, valid_token, commit=True
        )

        deleted_count = (
            self.password_reset_repository.delete_expired_password_reset_tokens(
                self.db, now=self._dt(2025, 1, 1), commit=True
            )
        )

        remaining_tokens = self.db.query(PasswordResetTokens).all()

        self.assertEqual(deleted_count, 1)
        self.assertEqual(len(remaining_tokens), 1)
        self.assertEqual(remaining_tokens[0].token_prefix, "newpw1")

    def test_delete_expired_password_reset_tokens_returns_zero_when_none_expired(self):
        valid_token = self._password_reset_token(
            token_prefix="validp",
            hashed_token="b" * 72,
            expires_at=self._dt(2030, 10, 20),
        )
        self.password_reset_repository.register_password_reset_token(
            self.db, valid_token, commit=True
        )

        deleted_count = (
            self.password_reset_repository.delete_expired_password_reset_tokens(
                self.db, now=self._dt(2025, 1, 1), commit=True
            )
        )

        self.assertEqual(deleted_count, 0)
