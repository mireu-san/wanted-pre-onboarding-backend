from django.test import TestCase
from rest_framework.test import APIClient
from SubmitHistoryApp.models import SubmitHistory
from JobPostingApp.models import JobPosting, TechStack, Company
from UserApp.models import User
from rest_framework import status
import datetime


class SubmitHistoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # User 객체 생성
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass"
        )

        # Company 객체 생성
        self.company = Company.objects.create(
            name="Example Company",
            description="This is an example company.",
            established_at=datetime.date.today(),  # 여기에 established_at 값을 추가합니다.
        )

        # TechStack 객체 생성
        self.tech1 = TechStack.objects.create(name="Python")
        self.tech2 = TechStack.objects.create(name="Django")

        # JobPosting 객체 생성
        self.job_posting = JobPosting.objects.create(
            company=self.company,  # 생성된 Company 객체를 사용
            position="Backend Developer",
            reward=60000,
            description="A job description...",
        )
        # JobPosting의 tech_stack 필드에 TechStack 객체 추가
        self.job_posting.tech_stack.add(self.tech1, self.tech2)

    def test_create_submit_history(self):
        response = self.client.post(
            "/submit_history/submit_histories/",
            {
                "user": self.user.id,
                "job_posting": self.job_posting.id,
                "status": "applied",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "user": self.user.id,
                "job_posting": self.job_posting.id,
                "status": "applied",
                "apply_date": response.data["apply_date"],
                "other_job_postings": [],
            },
        )

        # Validate the database state.
        submit_history = SubmitHistory.objects.get(id=1)
        self.assertEqual(submit_history.user.id, self.user.id)
        self.assertEqual(submit_history.job_posting.id, self.job_posting.id)
        self.assertEqual(submit_history.status, "applied")

    def test_submit_and_get_other_postings(self):
        # 다른 채용공고도 등록
        job_posting2 = JobPosting.objects.create(
            company=self.company,
            position="Frontend Developer",
            reward=900000,
            description="Hiring frontend devs.",
        )
        job_posting2.tech_stack.add(self.tech1)

        response = self.client.post(
            "/submit_history/submit_histories/",
            {
                "user": self.user.id,
                "job_posting": self.job_posting.id,
                "status": "applied",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("other_job_postings", response.data)
        other_postings = response.data["other_job_postings"]
        self.assertTrue(
            any(posting["id"] == job_posting2.id for posting in other_postings)
        )
