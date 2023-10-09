from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from CompanyApp.models import Company
from rest_framework import status


class CompanyAPITest(TestCase):
    def setUp(self):
        """테스트를 위한 사전 설정"""
        self.client = APIClient()
        self.company_data = {
            "name": "Paper Company",
            "country": "KR",
            "region": "Seoul",
            "description": "Sample description",
            "established_at": "2023-10-06",
            "founder": "Mr Kim",
        }
        self.company = Company.objects.create(**self.company_data)
        self.company_url = reverse("company-detail", kwargs={"pk": self.company.id})

    def test_retrieve_company(self):
        """특정 회사의 정보를 가져오는 API 테스트"""
        response = self.client.get(self.company_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.company_data["name"])

    def test_create_company(self):
        """회사를 새로 생성하는 API 테스트"""
        new_company_data = {
            "name": "Black Company",
            "country": "Snezhnaya",
            "region": "Seoul",
            "description": "Sample description for Paper Company",
            "established_at": "2020-01-01",
            "founder": "Queen",
        }
        response = self.client.post(reverse("company-list"), new_company_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], new_company_data["name"])

    def test_update_company(self):
        """회사 정보를 업데이트하는 API 테스트"""
        updated_data = {
            "name": "Updated Co.",
            "country": "US",
            "region": "NY",
            "description": "Updated description",
            "established_at": "2019-01-01",
            "founder": "Aiden Pearce",
        }
        response = self.client.put(self.company_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, updated_data["name"])
        self.assertEqual(self.company.country, updated_data["country"])

    def test_delete_company(self):
        """회사 정보를 삭제하는 API 테스트"""
        response = self.client.delete(self.company_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(id=self.company.id)

    def test_create_company_with_missing_name(self):
        """이름 필드 없이 회사 생성 API 호출 시 오류가 반환되는지 테스트"""
        incomplete_data = {
            "country": "Snezhnaya",
            "region": "Seoul",
            "description": "Sample description for Paper Company",
            "established_at": "2020-01-01",
            "founder": "Queen",
        }
        response = self.client.post(reverse("company-list"), incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_with_duplicate_name(self):
        """중복된 이름으로 회사 생성 API 호출 시 오류가 반환되는지 테스트"""
        response = self.client.post(reverse("company-list"), self.company_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_with_invalid_date(self):
        """유효하지 않은 날짜 형식으로 회사 생성 API 호출 시 오류가 반환되는지 테스트"""
        invalid_data = {
            "name": "Test Company",
            "country": "Snezhnaya",
            "region": "Seoul",
            "description": "Sample description for Paper Company",
            "established_at": "invalid_date",
            "founder": "Queen",
        }
        response = self.client.post(reverse("company-list"), invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
