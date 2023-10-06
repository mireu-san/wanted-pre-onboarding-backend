from rest_framework import viewsets, filters
from .models import JobPosting
from .serializers import JobPostingSerializer


class JobPostingViewSet(viewsets.ModelViewSet):
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
