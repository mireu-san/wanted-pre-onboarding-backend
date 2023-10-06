from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    establishment_duration = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"

    def get_establishment_duration(self, obj):
        return obj.get_establishment_duration()
