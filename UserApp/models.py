from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    """사용자 및 관리자 계정을 생성하기 위한 매니저"""

    def create_user(self, email, username, password=None, **extra_fields):
        """일반 사용자 생성 메서드"""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """슈퍼유저 생성 메서드"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """사용자 모델을 정의하는 클래스"""

    """
    is_active =  이 필드는 사용자가 활성 상태인지 표시
    is_staff = 관리자 사이트 접근 권한 여부
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """ groups, user_permissions 두 필드는 사용자 권한 관리를 위해 사용"""
    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="userapp_user_set",
        related_query_name="userapp_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="userapp_user_set",
        related_query_name="userapp_user",
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    class Meta:
        app_label = "UserApp"
