from django.db import models
from django.core.validators import MinValueValidator


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """Model representing a job posting."""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    reward = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    tech_stack = models.ManyToManyField(TechStack)

    def __str__(self):
        """String representation of a job posting."""
        return f"{self.position} at {self.company.name}"
