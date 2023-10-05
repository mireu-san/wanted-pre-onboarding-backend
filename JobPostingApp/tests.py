from django.test import TestCase
from rest_framework.test import APIClient
from .models import JobPosting


class JobPostingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_job_posting(self):
        response = self.client.post(
            "/job_posting/job_postings/",
            {
                "company_id": 1,
                "position": "Backend Developer",
                "reward": 1000000,
                "description": "We are hiring a backend developer...",
                "tech_stack": "Python, Django",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "company_id": 1,
                "position": "Backend Developer",
                "reward": 1000000,
                "description": "We are hiring a backend developer...",
                "tech_stack": "Python, Django",
            },
        )

        # Validate the database state.
        job_posting = JobPosting.objects.get(id=1)
        self.assertEqual(job_posting.position, "Backend Developer")
