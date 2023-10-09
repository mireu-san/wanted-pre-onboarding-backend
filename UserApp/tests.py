from rest_framework.test import APITestCase
from .models import User


class UserAPITest(APITestCase):
    """사용자 관련 API 테스트 케이스"""

    def test_create_user(self):
        """사용자 생성 API 테스트"""
        data = {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@example.com",  # 이메일 필드 추가
        }
        response = self.client.post("/user/users/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_retrieve_user(self):
        """특정 사용자 조회 API 테스트"""
        user = User.objects.create_user(
            email="retrieve@example.com", username="retrieveuser", password="testpass"
        )
        response = self.client.get(f"/user/users/{user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "retrieveuser")

    def test_update_user(self):
        """사용자 정보 수정 API 테스트"""
        user = User.objects.create_user(
            email="update@example.com", username="updateuser", password="testpass"
        )
        # API 호출 부분
        response = self.client.put(
            f"/user/users/{user.id}/",
            {
                "username": "updateduser",
                "email": "updated@example.com",
                "password": "newpassword123",  # API 로직: password 필수성 요구 (업데이트 시)
            },
            format="json",
        )
        # 응답의 상태 코드와 데이터 출력
        print(response.status_code)
        print(response.data)
        # 응답의 상태 코드와 데이터 검증
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    def test_delete_user(self):
        """사용자 삭제 API 테스트"""
        user = User.objects.create_user(
            email="delete@example.com", username="deleteuser", password="testpass"
        )
        response = self.client.delete(f"/user/users/{user.id}/")
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user.id)
