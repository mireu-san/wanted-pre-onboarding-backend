from django.test import TestCase
from rest_framework.test import APIClient
from .models import Company


class CompanyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Setup code...

    def test_create_company(self):
        response = self.client.post('/companies/', {'name': 'Test Co.', 'country': 'KR', 'region': 'Seoul'})
        self.assertEqual(response.status_code, 201)
