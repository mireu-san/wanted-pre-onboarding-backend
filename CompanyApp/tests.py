from django.test import TestCase
from rest_framework.test import APIClient
from CompanyApp.models import Company


class CompanyAPITest(TestCase):
    def setUp(self):
        # API 클라이언트를 초기화하고 테스트용 회사 데이터를 생성합니다.
        self.client = APIClient()
        self.company = Company.objects.create(
            name="Paper Company",
            country="KR",
            region="Seoul",
            description="Sample description",
            established_at="2023-10-06",
            founder="Mr Kim",
        )

    def test_retrieve_company(self):
        response = self.client.get(f"/company/companies/{self.company.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Paper Company")

    def test_create_company(self):
        response = self.client.post(
            "/company/companies/",
            {
                "name": "Black Company",
                "country": "Snezhnaya",
                "region": "Seoul",
                "description": "Sample description for Paper Company",
                "established_at": "2020-01-01",
                "founder": "Queen",
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Black Company")

    def test_update_company(self):
        # 회사 정보를 수정하는 API를 호출합니다.
        response = self.client.put(
            f"/company/companies/{self.company.id}/",
            {
                "name": "Updated Co.",
                "country": "US",
                "region": "NY",
                "description": "Updated description",
                "established_at": "2019-01-01",
                "founder": "Jane Smith",
            },
        )
        self.assertEqual(response.status_code, 200)
        # 수정된 정보를 확인합니다.
        self.company.refresh_from_db()  # 데이터베이스로부터 수정된 정보를 가져옵니다.
        self.assertEqual(self.company.name, "Updated Co.")
        self.assertEqual(self.company.country, "US")
        self.assertEqual(self.company.region, "NY")

    def test_delete_company(self):
        # 회사 정보를 삭제하는 API를 호출합니다.
        response = self.client.delete(f"/company/companies/{self.company.id}/")
        self.assertEqual(response.status_code, 204)  # 204: No Content (성공적으로 삭제됨)
        # 실제로 회사 정보가 삭제되었는지 확인합니다.
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(id=self.company.id)
