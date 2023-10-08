from rest_framework import serializers
from .models import SubmitHistory


class SubmitHistorySerializer(serializers.ModelSerializer):
    """제출 이력을 나타내는 시리얼라이저"""

    class Meta:
        model = SubmitHistory
        fields = "__all__"
