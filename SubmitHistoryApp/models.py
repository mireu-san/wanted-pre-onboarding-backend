from django.db import models
from UserApp.models import User
from JobPostingApp.models import JobPosting


class SubmitHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'job_posting']
