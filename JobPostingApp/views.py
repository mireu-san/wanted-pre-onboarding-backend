from rest_framework import viewsets, filters
from .models import JobPosting
from .serializers import JobPostingSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
    """
    채용 공고에 대한 API 엔드포인트.
    사용자는 직무, 회사 이름, 또는 기술 스택으로 검색 가능합니다.
    또한 reward, position 또는 company name으로 결과를 정렬할 수 있습니다.
    """

    queryset = JobPosting.objects.all().select_related("company")
    serializer_class = JobPostingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["position", "company__name", "tech_stack__name"]
    ordering_fields = ["reward", "position", "company__name"]
    ordering = ["company__name"]
