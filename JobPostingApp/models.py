from django.db import models
from django.core.validators import MinValueValidator
from CompanyApp.models import Company


class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """채용공고를 나타내는 모델."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE
    )  # CompanyApp에서의 Company 모델을 참조
    position = models.CharField(max_length=255)
    reward = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    tech_stack = models.ManyToManyField(TechStack)

    def __str__(self):
        """채용공고의 문자열 표현."""
        return f"{self.position} at {self.company.name}"
