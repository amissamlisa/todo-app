from backend.test.integration.test_base import TestBase
from uuid import uuid4


class TestTopAPI(TestBase):
    def _goal_save_payload(self):
        return {
            "goal": {
                "goal_name": "TOEIC800点取得",
                "status_against_goal": "現在TOEIC400点",
                "start_day": "2030-10-15",
                "target_day": "2030-10-22",
                "weekday_available_time": 90,
                "weekends_available_time": 180,
            },
            "goal_tasks": [],
            "goal_total_estimated_time": 60,
        }

    def _register_and_login(self):
        unique_suffix = uuid4().hex[:8]
        self.test_email = f"top_{unique_suffix}@example.com"
        self.test_username = f"top_user_{unique_suffix}"

        register_response = self.client.post(
            "/auth/registration",
            json={
                "username": self.test_username,
                "password": "ValidPass123!",
                "confirmation_password": "ValidPass123!",
                "email": self.test_email,
            },
        )
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/auth/login",
            data={
                "username": self.test_email,
                "password": "ValidPass123!",
            },
        )
        self.assertEqual(login_response.status_code, 200)
        return {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    def test_read_top_screen_info_success(self):
        headers = self._register_and_login()
        create_response = self.client.post(
            "/goal/", json=self._goal_save_payload(), headers=headers
        )
        self.assertEqual(create_response.status_code, 201)

        response = self.client.get("/top/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.test_username)
        self.assertEqual(response.json()["email"], self.test_email)
        self.assertIsNotNone(response.json()["goal"])
        self.assertEqual(response.json()["goal_tasks"], [])

    def test_read_top_screen_info_without_goal(self):
        headers = self._register_and_login()

        response = self.client.get("/top/", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.test_username)
        self.assertIsNone(response.json()["goal"])
        self.assertEqual(response.json()["goal_tasks"], [])

    def test_read_top_screen_info_unauthenticated(self):
        response = self.client.get("/top/")
        self.assertEqual(response.status_code, 401)


class TestSecurityHeaders(TestBase):
    def test_security_headers_are_set_on_response(self):
        response = self.client.get("/top/")

        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "deny")
        self.assertEqual(
            response.headers.get("Content-Security-Policy"),
            "default-src 'none'; frame-ancestors 'none'",
        )
