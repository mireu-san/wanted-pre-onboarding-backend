from rest_framework.response import Response
from JobPostingApp.serializers import JobPostingSerializer
from JobPostingApp.models import JobPosting

from rest_framework import viewsets, status
from .models import SubmitHistory
from .serializers import SubmitHistorySerializer


class SubmitHistoryViewSet(viewsets.ModelViewSet):
    """
    제출 이력을 보거나 편집할 수 있는 API 엔드포인트입니다.
    """

    queryset = SubmitHistory.objects.all()
    serializer_class = SubmitHistorySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            job_posting_id = request.data.get("job_posting")
            job_posting = JobPosting.objects.get(id=job_posting_id)
            company = job_posting.company

            other_job_postings = JobPosting.objects.filter(company=company).exclude(
                id=job_posting_id
            )
            other_job_postings_data = JobPostingSerializer(
                other_job_postings, many=True
            ).data

            response.data["other_job_postings"] = other_job_postings_data

        return response
