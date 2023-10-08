from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """사용자 모델의 시리얼라이저"""

    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
        ]  # 필요한 필드만 명시. 여기서 id는 DRF가 기본으로 제공

    def create(self, validated_data):
        """새 사용자 생성 메서드"""
        password = validated_data.pop("password", None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        """사용자 정보 업데이트 메서드"""
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
