from django.test import TestCase
from rest_framework.test import APIClient
from .models import JobPosting, Company, TechStack


class JobPostingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 예시 회사와 기술 스택 생성
        self.company = Company.objects.create(
            name="TechCorp", description="Leading tech company"
        )
        self.tech1 = TechStack.objects.create(name="Python")
        self.tech2 = TechStack.objects.create(name="Django")

    def test_create_job_posting(self):
        response = self.client.post(
            "/job_posting/job_postings/",
            {
                "company": self.company.id,
                "position": "Backend Developer",
                "reward": 1000000,
                "description": "We are hiring a backend developer...",
                "tech_stack": [self.tech1.id, self.tech2.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["position"], "Backend Developer")

        # Validate the database state.
        job_posting = JobPosting.objects.get(id=response.data["id"])
        self.assertEqual(job_posting.position, "Backend Developer")

    def test_retrieve_job_posting(self):
        job_posting = JobPosting.objects.create(
            company=self.company,
            position="Frontend Developer",
            reward=900000,
            description="Hiring frontend devs.",
        )
        job_posting.tech_stack.add(self.tech1)

        response = self.client.get(f"/job_posting/job_postings/{job_posting.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["position"], "Frontend Developer")

    def test_retrieve_other_job_postings_of_company(self):
        # 두 개의 채용공고를 해당 회사에 등록
        job_posting1 = JobPosting.objects.create(
            company=self.company,
            position="Frontend Developer",
            reward=900000,
            description="Hiring frontend devs.",
        )
        job_posting1.tech_stack.add(self.tech1)

        job_posting2 = JobPosting.objects.create(
            company=self.company,
            position="Backend Developer",
            reward=1100000,
            description="Hiring backend devs.",
        )
        job_posting2.tech_stack.add(self.tech2)

        # 첫 번째 채용공고를 조회
        response = self.client.get(f"/job_posting/job_postings/{job_posting1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["position"], "Frontend Developer")
        self.assertIn("other_job_postings", response.data)

        # 반환된 '다른 채용공고'에 두 번째 채용공고가 포함되어 있는지 확인
        other_postings = response.data["other_job_postings"]
        self.assertTrue(
            any(posting["id"] == job_posting2.id for posting in other_postings)
        )

    def test_update_job_posting(self):
        job_posting = JobPosting.objects.create(
            company=self.company,
            position="Fullstack Developer",
            reward=1200000,
            description="We need fullstack skills.",
        )
        job_posting.tech_stack.add(self.tech1, self.tech2)

        response = self.client.put(
            f"/job_posting/job_postings/{job_posting.id}/",
            {
                "company": self.company.id,
                "position": "Senior Fullstack Developer",
                "reward": 1400000,
                "description": "Senior devs needed.",
                "tech_stack": [self.tech1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        updated_job_posting = JobPosting.objects.get(id=job_posting.id)
        self.assertEqual(updated_job_posting.position, "Senior Fullstack Developer")

    def test_delete_job_posting(self):
        job_posting = JobPosting.objects.create(
            company=self.company,
            position="Data Scientist",
            reward=1300000,
            description="Data crunching experts needed.",
        )

        response = self.client.delete(f"/job_posting/job_postings/{job_posting.id}/")
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(JobPosting.DoesNotExist):
            JobPosting.objects.get(id=job_posting.id)
