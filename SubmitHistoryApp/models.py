from django.db import models
from UserApp.models import User
from JobPostingApp.models import JobPosting


class SubmitHistory(models.Model):
    """사용자의 지원 이력을 나타내는 모델"""

    STATUS_CHOICES = [
        ("applied", "지원완료"),
        ("rejected", "불합격"),
        ("accepted", "합격"),
    ]

    """
    user = 사용자 모델과의 외래키 관계
    job_posting = 채용공고 모델과의 외래키 관계
    status = 지원 상태
    apply_date = 지원 날짜
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    apply_date = models.DateTimeField(auto_now_add=True)

    """사용자와 채용공고의 조합은 유일해야 함"""

    class Meta:
        unique_together = [["user", "job_posting"]]
