from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    회사의 기본 세부 정보를 나타내는 모델입니다.
    """

    """
    name = 회사명은 중복을 허용하지 않습니다.
    description = 회사 설명란
    established_at = 회사 설립일
    founder = 창립자
    country = 국가
    region = 지역
    """
    name = models.CharField(max_length=100, unique=True)  # 이름은 유일하게 설정
    description = models.TextField()
    established_at = models.DateField()
    founder = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=100)

    """
    db_table = 테이블 이름을 명시적으로 정의
    ordering = 설립 날짜로 기본 정렬
    """

    class Meta:
        db_table = "companies"  # 테이블 이름을 명시적으로 정의
        ordering = ["established_at"]  # 설립 날짜로 기본 정렬

    def get_establishment_duration(self):
        """
        회사의 설립된 기간(연도 수)을 반환합니다. 예: 2022-10-06 -> 2023 기준, 1을 반환.
        """
        return (timezone.now().date() - self.established_at).days // 365
