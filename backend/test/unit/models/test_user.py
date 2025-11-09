from unittest import TestCase
from backend.models.models import Users


class UserTest(TestCase):
    # 初期化時に値が正しく設定された場合
    def test_create_goal(self):
        user = Users(
            username="sasa1231",
            hashed_password="abcd",
            email="abcde@example.com",
            user_points=100
        )

        self.assertEqual(user.username, "sasa1231",
                         "usernameの値が一致しません")
        self.assertEqual(user.hashed_password, "abcd",
                         "hashed_passwordの値が一致しません")
        self.assertEqual(user.email, "abcde@example.com",
                         "emailの値が一致しません")
        self.assertEqual(user.user_points, 100,
                         "user_pointsの値が一致しません")
