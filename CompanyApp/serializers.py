from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    establishment_duration = serializers.SerializerMethodField()

    class Meta:
        model = Company
        """ 모든 필드 포함 """
        fields = "__all__"

    def get_establishment_duration(self, obj):
        """
        회사 설립 이후 지난 연수를 계산하여 반환합니다. (예: 2022-10 -> 2023-10 개월 기준, 1을 반환)
        """
        return obj.get_establishment_duration()
