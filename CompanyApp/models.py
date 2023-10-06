from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    기본 세부 정보가 있는 회사를 대표하는 모델입니다.
    """

    name = models.CharField(
        max_length=100, unique=True
    )  # Considering the name to be unique
    description = models.TextField()
    established_at = models.DateField()
    founder = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=100)

    class Meta:
        db_table = "companies"  # Explicitly defining the table name
        ordering = ["established_at"]  # Default ordering by establishment date

    def get_establishment_duration(self):
        """
        회사가 설립된 연도를 return 합니다.
        """
        return (timezone.now().date() - self.established_at).days // 365
