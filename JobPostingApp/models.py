from django.db import models


class JobPosting(models.Model):
    """Model representing a job posting."""

    company_id = models.IntegerField()
    position = models.CharField(max_length=255)
    reward = models.IntegerField()
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)

    def __str__(self):
        """String representation of a job posting."""
        return f"{self.position} at Company ID {self.company_id}"
