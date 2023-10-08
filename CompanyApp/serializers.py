from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    establishment_duration = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_establishment_duration(self, obj):
        """
        회사의 설립된 기간(연도 수)을 반환합니다.
        """
        return obj.get_establishment_duration()
