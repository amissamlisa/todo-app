from backend.test.integration.test_base import TestBase
from unittest.mock import patch, Mock
from uuid import uuid4


class TestGoalTasksAPI(TestBase):
    def _registration_payload(self, *, username: str, email: str):
        return {
            "username": username,
            "password": "ValidPass123!",
            "confirmation_password": "ValidPass123!",
            "email": email,
        }

    def _goal_payload(self):
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

    def _goal_task_create_payload(self, **kwargs):
        payload = {
            "goal_task_name": "文法問題を解く",
            "deadline": "2030-10-21",
            "estimated_time": 45,
            "goal_task_status": "未着手",
        }
        payload.update(kwargs)
        return payload

    def _goal_tasks(self):
        get_response = self.client.get(
            f"/goal-tasks/{self.goal_id}", headers=self.headers
        )
        return get_response.json()["goal_tasks"]

    def _first_goal_task_id(self):
        return self._goal_tasks()[0]["goal_task_id"]

    def setUp(self):
        super().setUp()
        unique_suffix = uuid4().hex[:8]
        self.test_email = f"test_{unique_suffix}@example.com"
        self.test_username = f"testuser_{unique_suffix}"

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
        self.access_token = login_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        create_response = self.client.post(
            "/goal/", json=self._goal_payload(), headers=self.headers
        )
        self.assertEqual(create_response.status_code, 201)
        self.goal_id = create_response.json()["goal_id"]

        create_task_response = self.client.post(
            "/goal-tasks/",
            json=self._goal_task_create_payload(
                goal_task_name="単語学習",
                deadline="2030-10-18",
                estimated_time=60,
            ),
            headers=self.headers,
        )
        self.assertEqual(create_task_response.status_code, 201)

    def test_read_all_goal_tasks_success(self):
        response = self.client.get(f"/goal-tasks/{self.goal_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("goal_tasks", response.json())

    def test_read_goal_tasks_with_nonexistent_goal(self):
        response = self.client.get("/goal-tasks/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_read_goal_tasks_with_unauthenticated_user(self):
        response = self.client.get(f"/goal-tasks/{self.goal_id}")
        self.assertEqual(response.status_code, 401)

    def test_delete_goal_task_success(self):
        goal_task_id = self._first_goal_task_id()

        response = self.client.delete(
            f"/goal-tasks/{goal_task_id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_goal_task(self):
        response = self.client.delete("/goal-tasks/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_goal_task_with_unauthenticated_user(self):
        response = self.client.delete("/goal-tasks/1")
        self.assertEqual(response.status_code, 401)

    @patch("backend.routers.goal_tasks.OpenAI")
    def test_generate_goal_tasks_success(self, mock_openai):
        mock_response = Mock()
        mock_response.output_text = (
            '{"goal_tasks": [{"goal_task_name": "過去問演習", '
            '"deadline": "2030-10-20", "estimated_time": 60}]}'
        )
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_response
        mock_openai.return_value = mock_client

        payload = {
            "goal": {
                "goal_name": "TOEIC800点取得",
                "status_against_goal": "現在TOEIC400点",
                "start_day": "2030-10-15",
                "target_day": "2030-10-22",
                "weekday_available_time": 90,
                "weekends_available_time": 180,
                "task_creation_rule": "リーディングを中心にしたい",
            },
            "completed_goal_tasks_list": [],
        }

        response = self.client.post(
            "/goal-tasks/generate", json=payload, headers=self.headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["detail"], "目標達成タスクを生成しました")
        self.assertEqual(len(response.json()["goal_tasks"]), 1)

    def test_create_goal_task_success(self):
        payload = self._goal_task_create_payload()

        response = self.client.post("/goal-tasks/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["detail"], "目標達成タスクを登録しました")
        self.assertEqual(
            response.json()["goal_task"]["goal_task_name"], "文法問題を解く"
        )

    def test_create_goal_task_assigns_global_sequential_order_num(self):
        in_progress_payload = self._goal_task_create_payload(
            goal_task_name="リスニング演習",
            goal_task_status="作業中",
        )

        response = self.client.post(
            "/goal-tasks/", json=in_progress_payload, headers=self.headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["goal_task"]["order_num"], 2)

    def test_update_goal_task_order_success(self):
        create_payload = self._goal_task_create_payload()
        self.client.post("/goal-tasks/", json=create_payload, headers=self.headers)

        goal_tasks = self._goal_tasks()
        first_task = goal_tasks[0]
        second_task = goal_tasks[1]

        payload = {
            "from_goal_task_id": second_task["goal_task_id"],
            "to_goal_task_id": first_task["goal_task_id"],
            "from_goal_task_order": second_task["order_num"],
            "to_goal_task_order": first_task["order_num"],
        }
        response = self.client.put(
            "/goal-tasks/order", json=payload, headers=self.headers
        )
        self.assertEqual(response.status_code, 204)

        updated = self.client.get(f"/goal-tasks/{self.goal_id}", headers=self.headers)
        updated_tasks = updated.json()["goal_tasks"]
        self.assertEqual(updated_tasks[0]["goal_task_id"], second_task["goal_task_id"])

    def test_update_goal_task_status_and_order_success(self):
        goal_task_id = self._first_goal_task_id()

        payload = {
            "order_num": 1,
            "new_status": "作業中",
        }
        response = self.client.put(
            f"/goal-tasks/status/{goal_task_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)

        updated = self.client.get(f"/goal-tasks/{self.goal_id}", headers=self.headers)
        self.assertEqual(updated.json()["goal_tasks"][0]["goal_task_status"], "作業中")

    def test_update_goal_task_success(self):
        goal_task_id = self._first_goal_task_id()

        payload = {
            "goal_task_name": "英単語100語復習",
            "deadline": "2030-10-21",
            "estimated_time": 30,
        }
        response = self.client.put(
            f"/goal-tasks/{goal_task_id}", json=payload, headers=self.headers
        )
        self.assertEqual(response.status_code, 204)

        updated = self.client.get(f"/goal-tasks/{self.goal_id}", headers=self.headers)
        self.assertEqual(
            updated.json()["goal_tasks"][0]["goal_task_name"], "英単語100語復習"
        )
