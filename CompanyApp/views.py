from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    기업을 보거나 편집할 수 있는 API 엔드포인트입니다.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
