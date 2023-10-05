from django.test import TestCase
from rest_framework.test import APIClient
from CompanyApp.models import Company


class CompanyAPITest(TestCase):
    def setUp(self):
        # API 클라이언트를 초기화합니다.
        self.client = APIClient()

    def test_create_company(self):
        # API를 호출하여 회사를 생성합니다.
        response = self.client.post(
            "/company/companies/",
            {"name": "Test Co.", "country": "KR", "region": "Seoul"},
        )
        # 상태 코드를 검사하여 요청이 성공적으로 이루어졌는지 확인합니다. (201: 생성됨)
        self.assertEqual(response.status_code, 201)

        # 응답 데이터를 검사하여 예상된 값과 일치하는지 확인합니다. (선택적이지만 권장됩니다.)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Test Co.",
                "country": "KR",
                "region": "Seoul",
            },
        )

        # 데이터베이스의 상태를 검사하여 실제로 회사 객체가 올바르게 생성되었는지 확인합니다. (선택적이지만 권장됩니다.)
        company = Company.objects.get(id=1)
        self.assertEqual(company.name, "Test Co.")
        self.assertEqual(company.country, "KR")
        self.assertEqual(company.region, "Seoul")
