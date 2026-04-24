from backend.test.integration.test_base import TestBase


def _registration_payload():
    return {
        "username": "testuser",
        "password": "ValidPass123!",
        "confirmation_password": "ValidPass123!",
        "email": "test@example.com",
    }


def _login_form():
    return {
        "username": "test@example.com",
        "password": "ValidPass123!",
    }


class TestUserPointsUpdate(TestBase):
    def _create_and_login(self):
        self.client.post("/auth/registration", json=_registration_payload())
        response = self.client.post("/auth/login", data=_login_form())
        return response.json()["access_token"]

    def _auth_headers(self):
        token = self._create_and_login()
        return {"Authorization": f"Bearer {token}"}

    def test_update_points_success(self):
        response = self.client.put(
            "/users/points",
            json={"points": 100},
            headers=self._auth_headers(),
        )
        self.assertEqual(response.status_code, 204)

    def test_update_points_without_auth(self):
        response = self.client.put(
            "/users/points",
            json={"points": 100},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_points_with_negative_value(self):
        response = self.client.put(
            "/users/points",
            json={"points": -10},
            headers=self._auth_headers(),
        )
        self.assertEqual(response.status_code, 422)


class TestUserRankUpdate(TestBase):
    def _create_and_login(self):
        self.client.post("/auth/registration", json=_registration_payload())
        response = self.client.post("/auth/login", data=_login_form())
        return response.json()["access_token"]

    def _auth_headers(self):
        token = self._create_and_login()
        return {"Authorization": f"Bearer {token}"}

    def test_update_rank_success(self):
        response = self.client.put(
            "/users/rank",
            json={"user_rank": "霧"},
            headers=self._auth_headers(),
        )
        self.assertEqual(response.status_code, 204)

    def test_update_rank_without_auth(self):
        response = self.client.put(
            "/users/rank",
            json={"user_rank": "霧"},
        )
        self.assertEqual(response.status_code, 401)
