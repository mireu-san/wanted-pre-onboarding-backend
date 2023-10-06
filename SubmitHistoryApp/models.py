from django.db import models
from UserApp.models import User
from JobPostingApp.models import JobPosting


class SubmitHistory(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    apply_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "job_posting"]]
