from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from SubmitHistoryApp.models import SubmitHistory
from JobPostingApp.models import JobPosting, TechStack, Company
from UserApp.models import User
from rest_framework import status
import datetime


class SubmitHistoryAPITest(TestCase):
    """
    제출 이력에 관한 테스트 케이스 클래스입니다.
    이 클래스는 SubmitHistory 모델과 관련된 API의 테스트를 담당합니다.
    """

    def setUp(self):
        """
        테스트 데이터 초기 설정 메서드입니다.
        이 메서드에서는 테스트에 필요한 User, Company, TechStack, JobPosting 객체를 생성합니다.
        """
        self.client = APIClient()

        """
        User 객체를 생성합니다. 이메일, 사용자 이름, 비밀번호를 설정합니다.
        """
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass"
        )

        # Company 객체 생성
        """
        Company 객체를 생성합니다. 회사 이름, 설명, 설립 날짜를 설정합니다.
        """
        self.company = Company.objects.create(
            name="Example Company",
            description="This is an example company.",
            established_at=datetime.date.today(),
        )

        """
        TechStack 객체를 두 개 생성합니다. 하나는 Python, 다른 하나는 Django를 나타냅니다.
        """
        self.tech1 = TechStack.objects.create(name="Python")
        self.tech2 = TechStack.objects.create(name="Django")

        """
        JobPosting 객체를 생성합니다. 회사, 직위, 보상, 설명을 설정합니다.
        """
        self.job_posting = JobPosting.objects.create(
            company=self.company,
            position="Backend Developer",
            reward=60000,
            description="A job description...",
        )
        # JobPosting의 tech_stack 필드에 TechStack 객체 추가
        """
        JobPosting의 tech_stack 필드에 앞서 생성한 두 TechStack 객체를 추가합니다.
        """
        self.job_posting.tech_stack.add(self.tech1, self.tech2)

    def create_submit_history(self, user, job_posting, status):
        """
        제출 이력 생성을 돕는 헬퍼 함수입니다.
        이 함수는 주어진 사용자, 채용공고, 상태 값으로 제출 이력을 생성하고 응답을 반환합니다.
        """
        url = reverse("submithistory-list")
        response = self.client.post(
            url,
            {
                "user": user.id,
                "job_posting": job_posting.id,
                "status": status,
            },
        )
        return response

    def test_create_submit_history(self):
        """
        제출 이력 생성에 대한 테스트 메서드입니다.
        이 메서드는 제출 이력 생성 API가 올바르게 동작하는지 확인합니다.
        """
        response = self.create_submit_history(self.user, self.job_posting, "applied")
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

        """
        데이터베이스의 상태를 검증하여 제출 이력이 올바르게 생성되었는지 확인합니다.
        """
        submit_history = SubmitHistory.objects.get(id=1)
        self.assertEqual(submit_history.user.id, self.user.id)
        self.assertEqual(submit_history.job_posting.id, self.job_posting.id)
        self.assertEqual(submit_history.status, "applied")

    def test_submit_and_get_other_postings(self):
        """
        지원 시 해당 회사의 다른 채용공고 정보 반환에 대한 테스트 메서드입니다.
        이 메서드는 사용자가 지원하면 해당 회사의 다른 채용공고 정보를 반환하는지 확인합니다.
        """
        job_posting2 = JobPosting.objects.create(
            company=self.company,
            position="Frontend Developer",
            reward=900000,
            description="Hiring frontend devs.",
        )
        job_posting2.tech_stack.add(self.tech1)

        response = self.create_submit_history(self.user, self.job_posting, "applied")

        self.assertEqual(response.status_code, 201)
        self.assertIn("other_job_postings", response.data)
        other_postings = response.data["other_job_postings"]
        self.assertTrue(
            any(posting["id"] == job_posting2.id for posting in other_postings)
        )
