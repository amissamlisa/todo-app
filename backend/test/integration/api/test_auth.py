from backend.test.integration.test_base import TestBase
from unittest.mock import patch

from backend.repository.repository import RefreshTokenRepository, UserRepository
from backend.utils.auth_helpers import create_password_reset_token


def _registration_payload(**kwargs):
    payload = {
        "username": "testuser",
        "password": "ValidPass123!",
        "confirmation_password": "ValidPass123!",
        "email": "test@example.com",
    }
    payload.update(kwargs)
    return payload


def _login_form(password="ValidPass123!", username="test@example.com"):
    return {
        "username": username,
        "password": password,
    }


class TestUserRegistration(TestBase):
    def _register(self, **kwargs):
        return self.client.post(
            "/auth/registration", json=_registration_payload(**kwargs)
        )

    def test_register_user_success(self):
        response = self._register()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "The user has been registered successfully"
        )

    def test_register_user_with_email_already_registered(self):
        self._register(username="user1", email="user1@example.com")

        response = self._register(
            username="user2",
            password="ValidPass456!",
            confirmation_password="ValidPass456!",
            email="user1@example.com",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error_code"], "EMAIL_ALREADY_REGISTERED")

    def test_register_user_with_short_password(self):
        response = self._register(password="Short1!", confirmation_password="Short1!")
        self.assertEqual(response.status_code, 422)

    def test_register_user_with_password_mismatch(self):
        response = self._register(confirmation_password="DifferentPass123!")
        self.assertEqual(response.status_code, 422)

    def test_register_user_with_invalid_email(self):
        response = self._register(email="invalid-email")
        self.assertEqual(response.status_code, 422)

    def test_register_user_with_empty_username(self):
        response = self._register(username="")
        self.assertEqual(response.status_code, 422)


class TestUserLogin(TestBase):
    def _register_user(self):
        self.client.post("/auth/registration", json=_registration_payload())

    def test_login_success(self):
        self._register_user()
        response = self.client.post("/auth/login", data=_login_form())
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")
        self.assertIn("refresh_token=", response.headers.get("set-cookie", ""))

    def test_login_with_invalid_credentials(self):
        self._register_user()
        response = self.client.post(
            "/auth/login", data=_login_form(password="WrongPassword123!")
        )
        self.assertEqual(response.status_code, 401)

    def test_login_with_nonexistent_user(self):
        response = self.client.post(
            "/auth/login",
            data=_login_form(
                username="nonexistent@example.com", password="SomePass123!"
            ),
        )
        self.assertEqual(response.status_code, 401)


class TestTokenLifecycle(TestBase):
    def _register_and_login(self):
        self.client.post("/auth/registration", json=_registration_payload())
        return self.client.post("/auth/login", data=_login_form())

    def test_refresh_success(self):
        self.client.cookies.clear()
        login_response = self._register_and_login()
        self.assertEqual(login_response.status_code, 200)

        response = self.client.post("/auth/refresh")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")
        self.assertIn("refresh_token=", response.headers.get("set-cookie", ""))

    def test_refresh_without_cookie(self):
        self.client.cookies.clear()

        response = self.client.post("/auth/refresh")

        self.assertEqual(response.status_code, 401)

    def test_refresh_with_revoked_token_reuse_detected(self):
        self.client.cookies.clear()
        login_response = self._register_and_login()
        self.assertEqual(login_response.status_code, 200)
        old_refresh_token = self.client.cookies.get("refresh_token")

        refresh_response = self.client.post("/auth/refresh")
        self.assertEqual(refresh_response.status_code, 200)

        self.client.cookies.set("refresh_token", old_refresh_token)
        reuse_response = self.client.post("/auth/refresh")

        self.assertEqual(reuse_response.status_code, 401)
        self.assertEqual(
            reuse_response.json()["error_code"], "REFRESH_TOKEN_REUSE_DETECTED"
        )

    def test_logout_success(self):
        self.client.cookies.clear()
        login_response = self._register_and_login()
        self.assertEqual(login_response.status_code, 200)

        response = self.client.delete("/auth/logout")

        self.assertEqual(response.status_code, 204)
        self.assertIn("refresh_token=", response.headers.get("set-cookie", ""))
        self.assertIn("Max-Age=0", response.headers.get("set-cookie", ""))

    def test_logout_without_cookie(self):
        self.client.cookies.clear()

        response = self.client.delete("/auth/logout")

        self.assertEqual(response.status_code, 401)


class TestPasswordReset(TestBase):
    def _register_user(self):
        response = self.client.post("/auth/registration", json=_registration_payload())
        self.assertEqual(response.status_code, 201)
        return UserRepository().find_user_by_email(self.db, "test@example.com")

    def test_password_reset_request_success(self):
        self._register_user()

        with patch("backend.routers.auth.send_email") as mock_send_email:
            response = self.client.post(
                "/auth/password-reset/request",
                json={"email": "test@example.com"},
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "A password reset link has been sent"
        )
        mock_send_email.assert_called_once()

    def test_password_reset_request_with_invalid_email(self):
        response = self.client.post(
            "/auth/password-reset/request",
            json={"email": "missing@example.com"},
        )

        self.assertEqual(response.status_code, 404)

    def test_password_reset_verification_success(self):
        user = self._register_user()
        token = create_password_reset_token(user.user_id, self.db)

        response = self.client.get(f"/auth/password-reset/verification?token={token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Valid password reset link")

    def test_password_reset_verification_with_invalid_token(self):
        response = self.client.get(
            "/auth/password-reset/verification?token=invalid-token"
        )

        self.assertEqual(response.status_code, 404)

    def test_reset_password_success(self):
        user = self._register_user()
        self.client.post("/auth/login", data=_login_form())
        token = create_password_reset_token(user.user_id, self.db)

        response = self.client.put(
            "/auth/password-reset",
            json={
                "password": "NewValidPass123!",
                "token": token,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "Password has been reset successfully"
        )

        old_login_response = self.client.post("/auth/login", data=_login_form())
        self.assertEqual(old_login_response.status_code, 401)

        new_login_response = self.client.post(
            "/auth/login", data=_login_form(password="NewValidPass123!")
        )
        self.assertEqual(new_login_response.status_code, 200)

    def test_reset_password_revokes_all_refresh_tokens(self):
        user = self._register_user()
        self.client.post("/auth/login", data=_login_form())
        token = create_password_reset_token(user.user_id, self.db)

        response = self.client.put(
            "/auth/password-reset",
            json={
                "password": "NewValidPass123!",
                "token": token,
            },
        )
        self.assertEqual(response.status_code, 201)

        revoked_count = RefreshTokenRepository().revoke_all_user_tokens(
            self.db, user.user_id, commit=True
        )
        self.assertEqual(revoked_count, 0)

    def test_reset_password_with_invalid_token(self):
        self._register_user()

        response = self.client.put(
            "/auth/password-reset",
            json={
                "password": "NewValidPass123!",
                "token": "invalid-token",
            },
        )

        self.assertEqual(response.status_code, 404)
