from unittest import TestCase

from pydantic import ValidationError

from backend.schemas.schemas import (
    PasswordResetEmailRequest,
    PasswordResetRequest,
    Token,
    UserPointsUpdateRequest,
    UserRankUpdateRequest,
    UserRequest,
)


class TestUserRequest(TestCase):
    def _valid_payload(self, **kwargs):
        defaults = dict(
            username="user1",
            password="Password1!",
            confirmation_password="Password1!",
            email="test@example.com",
        )
        defaults.update(kwargs)
        return defaults

    def test_user_request_accepts_valid_payload(self):
        req = UserRequest(**self._valid_payload())
        self.assertEqual(req.username, "user1")

    def test_user_request_with_empty_username_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(**self._valid_payload(username=""))

    def test_user_request_with_invalid_email_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(**self._valid_payload(email="not-an-email"))

    def test_user_request_with_too_short_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(password="Pass1!", confirmation_password="Pass1!")
            )

    def test_user_request_without_uppercase_in_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(
                    password="password1!", confirmation_password="password1!"
                )
            )

    def test_user_request_without_lowercase_in_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(
                    password="PASSWORD1!", confirmation_password="PASSWORD1!"
                )
            )

    def test_user_request_without_digit_in_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(
                    password="Password!!", confirmation_password="Password!!"
                )
            )

    def test_user_request_without_symbol_in_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(
                    password="Password123", confirmation_password="Password123"
                )
            )

    def test_user_request_with_password_mismatch_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            UserRequest(
                **self._valid_payload(
                    password="Password1!",
                    confirmation_password="Different1!",
                )
            )


class TestUserPointsUpdateRequest(TestCase):
    def test_user_points_update_request_accepts_zero(self):
        req = UserPointsUpdateRequest(points=0)
        self.assertEqual(req.points, 0)

    def test_user_points_update_request_accepts_positive_points(self):
        req = UserPointsUpdateRequest(points=100)
        self.assertEqual(req.points, 100)

    def test_user_points_update_request_with_negative_points_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            UserPointsUpdateRequest(points=-1)


class TestUserRankUpdateRequest(TestCase):
    def test_user_rank_update_request_accepts_valid_rank(self):
        req = UserRankUpdateRequest(user_rank="雫")
        self.assertEqual(req.user_rank, "雫")

    def test_user_rank_update_request_accepts_empty_rank(self):
        req = UserRankUpdateRequest(user_rank="")
        self.assertEqual(req.user_rank, "")


class TestPasswordResetSchemas(TestCase):
    def test_password_reset_email_request_accepts_valid_email(self):
        req = PasswordResetEmailRequest(email="test@example.com")
        self.assertEqual(req.email, "test@example.com")

    def test_password_reset_email_request_with_invalid_email_raises_validation_error(
        self,
    ):
        with self.assertRaises(ValidationError):
            PasswordResetEmailRequest(email="not-an-email")

    def test_password_reset_request_accepts_valid_payload(self):
        req = PasswordResetRequest(password="NewValidPass123!", token="token-value")
        self.assertEqual(req.token, "token-value")

    def test_password_reset_request_with_none_token_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            PasswordResetRequest(password="NewValidPass123!", token=None)

    def test_password_reset_request_with_short_password_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            PasswordResetRequest(password="short1!", token="token-value")


class TestTokenSchema(TestCase):
    def test_token_accepts_valid_payload(self):
        req = Token(access_token="access-token", token_type="bearer")
        self.assertEqual(req.token_type, "bearer")
