from django.test import TestCase
from rest_framework.test import APIClient
from .models import User


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        response = self.client.post('/users/', {
            'username': 'testuser',
            'email': 'test@example.com',
            # 여기에 추가적인 필드를 넣을 수 있습니다.
        })
        self.assertEqual(response.status_code, 201)
