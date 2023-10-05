from rest_framework.test import APITestCase
from .models import User


class UserAPITest(APITestCase):
    def test_create_user(self):
        data = {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@example.com",  # 이메일 필드 추가
        }
        response = self.client.post("/user/", data, format="json")
        self.assertEqual(response.status_code, 201)
