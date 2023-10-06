from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자를 보거나 편집할 수 있는 API 엔드포인트입니다.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
