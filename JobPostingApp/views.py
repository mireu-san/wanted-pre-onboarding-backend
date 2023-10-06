from rest_framework import viewsets, filters
from .models import JobPosting
from .serializers import JobPostingSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    """
    채용 공고를 보거나 편집할 수 있는 API 엔드포인트입니다.
    사용자는 position, company name 또는 기술 스택으로 검색할 수 있습니다.
    또한 reward, position 또는 company name 별로 결과를 정렬할 수도 있습니다.
    """

    queryset = (
        JobPosting.objects.all()
        .select_related("company")
        .prefetch_related("tech_stack")
    )
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["position", "company__name", "tech_stack__name"]
    ordering_fields = ["reward", "position", "company__name"]
    ordering = ["company__name"]
