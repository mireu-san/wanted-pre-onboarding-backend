from rest_framework import viewsets
from .models import SubmitHistory
from .serializers import SubmitHistorySerializer


class SubmitHistoryViewSet(viewsets.ModelViewSet):
    queryset = SubmitHistory.objects.all()
    serializer_class = SubmitHistorySerializer
