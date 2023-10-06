from rest_framework import viewsets
from .models import SubmitHistory
from .serializers import SubmitHistorySerializer


class SubmitHistoryViewSet(viewsets.ModelViewSet):
    """
    제출 이력을 보거나 편집할 수 있는 API 엔드포인트입니다.
    """

    queryset = SubmitHistory.objects.all()
    serializer_class = SubmitHistorySerializer
