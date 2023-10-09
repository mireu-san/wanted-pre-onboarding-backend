from rest_framework import viewsets, filters
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """회사 정보를 조회하거나 편집할 수 있는 CRUD API 엔드포인트입니다."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    """검색 기능 - 이름, 설명, 설립자, 국가, 지역"""
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "founder", "country", "region"]
