from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    # 여기에 추가적인 필드를 넣을 수 있습니다.
    # 예: 프로필 사진, 자기소개 등
