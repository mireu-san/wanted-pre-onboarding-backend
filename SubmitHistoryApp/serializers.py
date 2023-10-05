from rest_framework import serializers
from .models import SubmitHistory


class SubmitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitHistory
        fields = '__all__'
