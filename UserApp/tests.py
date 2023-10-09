from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


class UserAPITest(APITestCase):
    """
    사용자 관련 API 테스트 케이스 클래스입니다.
    이 클래스는 User 모델과 관련된 API의 테스트를 담당합니다.
    """

    def create_user(self, username, email, password):
        """
        사용자 생성 헬퍼 메서드입니다.
        """
        data = {
            "username": username,
            "password": password,
            "email": email,
        }
        url = reverse("user-list")
        return self.client.post(url, data, format="json")

    def test_create_user(self):
        """
        사용자 생성 API 테스트 메서드입니다.
        이 메서드는 사용자 생성 API가 올바르게 동작하는지 확인합니다.
        """
        response = self.create_user("testuser", "testuser@example.com", "testpass")
        self.assertEqual(response.status_code, 201)

    def test_retrieve_user(self):
        """
        특정 사용자 조회 API 테스트 메서드입니다.
        이 메서드는 특정 사용자를 조회하는 API가 올바르게 동작하는지 확인합니다.
        """
        user = User.objects.create_user(
            email="retrieve@example.com", username="retrieveuser", password="testpass"
        )
        url = reverse("user-detail", kwargs={"pk": user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "retrieveuser")

    def test_update_user(self):
        """
        사용자 정보 수정 API 테스트 메서드입니다.
        이 메서드는 사용자 정보를 수정하는 API가 올바르게 동작하는지 확인합니다.
        """
        user = User.objects.create_user(
            email="update@example.com", username="updateuser", password="testpass"
        )
        url = reverse("user-detail", kwargs={"pk": user.id})
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "password": "newpassword123",  # API 로직: password 필수성 요구 (업데이트 시)
        }
        response = self.client.put(url, data, format="json")
        # 응답의 상태 코드와 데이터 검증
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    def test_delete_user(self):
        """
        사용자 삭제 API 테스트 메서드입니다.
        이 메서드는 사용자를 삭제하는 API가 올바르게 동작하는지 확인합니다.
        """
        user = User.objects.create_user(
            email="delete@example.com", username="deleteuser", password="testpass"
        )
        url = reverse("user-detail", kwargs={"pk": user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user.id)
