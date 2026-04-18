from backend.test.integration.test_base import TestBase
from uuid import uuid4


class TestGoalAPI(TestBase):
    def _registration_payload(self, **kwargs):
        payload = {
            "username": "testuser",
            "password": "ValidPass123!",
            "confirmation_password": "ValidPass123!",
            "email": "test@example.com",
        }
        payload.update(kwargs)
        return payload

    def _goal_save_payload(self, **kwargs):
        payload = {
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
        payload.update(kwargs)
        return payload

    def _create_goal(self, payload=None):
        create_payload = payload or self._goal_save_payload()
        return self.client.post("/goal/", json=create_payload, headers=self.headers)

    def _register_and_login(self):
        unique_suffix = uuid4().hex[:8]
        self.test_email = f"goal_{unique_suffix}@example.com"
        self.test_username = f"goal_user_{unique_suffix}"

        register_response = self.client.post(
            "/auth/registration",
            json=self._registration_payload(
                username=self.test_username,
                email=self.test_email,
            ),
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
        return login_response.json()["access_token"]

    def setUp(self):
        super().setUp()
        self.access_token = self._register_and_login()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def test_save_goal_and_goal_tasks_success(self):
        response = self._create_goal(
            self._goal_save_payload(
                goal_tasks=[
                    {
                        "goal_task_name": "単語学習",
                        "deadline": "2030-10-18",
                        "estimated_time": 60,
                        "goal_task_status": "未着手",
                    }
                ],
                goal={
                    "goal_name": "TOEIC800点取得",
                    "status_against_goal": "現在TOEIC400点",
                    "start_day": "2030-10-15",
                    "target_day": "2030-10-22",
                    "weekday_available_time": 90,
                    "weekends_available_time": 180,
                    "task_creation_rule": "リーディングを中心にしたい",
                },
            )
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("goal_id", response.json())
        self.assertEqual(
            response.json()["detail"], "達成目標と目標達成タスクが保存されました"
        )

    def test_save_goal_with_unauthenticated_user(self):
        response = self.client.post("/goal/", json=self._goal_save_payload())
        self.assertEqual(response.status_code, 401)

    def test_read_goal_success(self):
        create_response = self._create_goal()
        goal_id = create_response.json()["goal_id"]

        response = self.client.get(f"/goal/{goal_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("goal", response.json())

    def test_read_nonexistent_goal(self):
        response = self.client.get("/goal/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_goal_success(self):
        create_response = self._create_goal()
        goal_id = create_response.json()["goal_id"]

        response = self.client.delete(f"/goal/{goal_id}", headers=self.headers)
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_goal(self):
        response = self.client.delete("/goal/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_goal_status_to_achieved(self):
        create_response = self._create_goal()
        goal_id = create_response.json()["goal_id"]

        response = self.client.patch(
            f"/goal/{goal_id}?new_status=達成",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)
