from django.test import TestCase
from rest_framework.test import APIClient
from CompanyApp.models import Company
from .models import JobPosting


class JobPostingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(
            name="TestCompany", country="Korea", region="Seoul"
        )
        self.job_posting = JobPosting.objects.create(
            company=self.company,
            position="Backend Developer",
            reward=1000000,
            content="We are hiring a backend developer...",
            technology="Python",
        )

    def test_create_job_posting(self):
        response = self.client.post(
            "/job_postings/",
            {
                "company_id": self.company.id,
                "position": "Frontend Developer",
                "reward": 1200000,
                "content": "We are hiring a frontend developer...",
                "technology": "JavaScript",
            },
        )
        self.assertEqual(response.status_code, 201)
