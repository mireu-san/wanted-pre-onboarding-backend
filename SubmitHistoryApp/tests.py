from django.test import TestCase
from rest_framework.test import APIClient
from UserApp.models import User
from JobPostingApp.models import JobPosting
from .models import SubmitHistory


class SubmitHistoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", email="test@example.com")
        self.job_posting = JobPosting.objects.create(
            company_id=1,
            position="Example Position",
            reward=100000,
            content="Example Content",
            technology="Python",
            # 다른 필요한 필드들...
        )

    def test_create_submit_history(self):
        response = self.client.post(
            "/submit_history/",
            {
                "user_id": self.user.id,
                "job_posting_id": self.job_posting.id,
            },
        )
        self.assertEqual(response.status_code, 201)
