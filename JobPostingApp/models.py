from django.db import models
from CompanyApp.models import Company


class JobPosting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    reward = models.IntegerField()
    content = models.TextField()
    technology = models.CharField(max_length=50)

    class Meta:
        app_label = "JobPostingApp"
