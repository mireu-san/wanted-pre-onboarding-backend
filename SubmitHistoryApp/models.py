from django.db import models
from UserApp.models import User
from JobPostingApp.models import JobPosting


class SubmitHistory(models.Model):
    user_id = models.IntegerField()
    job_posting_id = models.IntegerField()
    status = models.CharField(max_length=255)
    apply_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user_id", "job_posting_id"]]
