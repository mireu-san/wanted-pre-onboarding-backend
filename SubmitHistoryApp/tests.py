from django.test import TestCase
from rest_framework.test import APIClient
from SubmitHistoryApp.models import SubmitHistory
from JobPostingApp.models import JobPosting


class SubmitHistoryAPITest(TestCase):
    def setUp(self):
        self.job_posting = JobPosting.objects.create(
            company_id=1,
            position="Backend Developer",
            reward=60000,
            description="A job description...",
            tech_stack="Python, Django",
        )

    def test_create_submit_history(self):
        response = self.client.post(
            "/submit_history/submit_histories/",
            {
                "user_id": 1,
                "job_posting_id": self.job_posting.id,
                "status": "applied",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "user_id": 1,
                "job_posting_id": self.job_posting.id,
                "status": "applied",
                "apply_date": response.data[
                    "apply_date"
                ],  # auto_now_add 필드는 클라이언트에서 설정되지 않습니다.
            },
        )

        # Validate the database state.
        submit_history = SubmitHistory.objects.get(id=1)
        self.assertEqual(submit_history.user_id, 1)
        self.assertEqual(submit_history.job_posting_id, self.job_posting.id)
        self.assertEqual(submit_history.status, "applied")
