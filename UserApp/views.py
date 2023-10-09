from rest_framework import viewsets, filters
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    """사용자 관련 API를 제공하는 뷰셋"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    """검색 - 이메일, 사용자명"""
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "username"]
