from django.db import models
from django.core.validators import MinValueValidator
from CompanyApp.models import Company


class TechStack(models.Model):
    """기술 스택을 나타내는 모델. 예: Python, Django 등"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """채용공고를 나타내는 모델."""

    """ 
    CompanyApp에서의 Company 모델을 참조
    Company 모델과의 ForeignKey 관계
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    reward = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    """ 기술 스택과의 다대다 관계 (admin 페이지에서 추가 가능) """
    tech_stack = models.ManyToManyField(TechStack)

    def __str__(self):
        """채용공고의 문자열 표현을 반환합니다."""
        return f"{self.position} at {self.company.name}"
