import datetime
from unittest import TestCase

from backend.models.models import PasswordResetTokens, RefreshTokens


class TestRefreshTokenModel(TestCase):
    def _dt(self, year, month, day):
        return datetime.datetime(year, month, day, 12, 0, tzinfo=datetime.timezone.utc)

    def _refresh_token(self, **kwargs):
        defaults = dict(
            user_id=1,
            token_prefix="abcdef",
            hashed_token="a" * 72,
            expires_at=self._dt(2030, 10, 15),
        )
        defaults.update(kwargs)
        return RefreshTokens(**defaults)

    def _password_reset_token(self, **kwargs):
        defaults = dict(
            user_id=1,
            token_prefix="ghijkl",
            hashed_token="c" * 72,
            expires_at=self._dt(2030, 10, 20),
        )
        defaults.update(kwargs)
        return PasswordResetTokens(**defaults)

    def test_refresh_token_sets_all_fields_correctly(self):
        revoked_at = self._dt(2030, 10, 16)
        refresh_token = self._refresh_token(revoked_at=revoked_at)
        expires_at = self._dt(2030, 10, 15)
        self.assertEqual(
            (
                refresh_token.user_id,
                refresh_token.token_prefix,
                refresh_token.hashed_token,
                refresh_token.expires_at,
                refresh_token.revoked_at,
            ),
            (1, "abcdef", "a" * 72, expires_at, revoked_at),
        )

    def test_refresh_token_allows_none_revoked_at(self):
        refresh_token = self._refresh_token(hashed_token="b" * 72, revoked_at=None)
        self.assertIsNone(refresh_token.revoked_at)

    def test_password_reset_token_sets_all_fields_correctly(self):
        expires_at = self._dt(2030, 10, 20)
        password_reset_token = self._password_reset_token()
        self.assertEqual(
            (
                password_reset_token.user_id,
                password_reset_token.token_prefix,
                password_reset_token.hashed_token,
                password_reset_token.expires_at,
            ),
            (1, "ghijkl", "c" * 72, expires_at),
        )
