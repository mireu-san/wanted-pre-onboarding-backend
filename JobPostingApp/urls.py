from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"job_postings", views.JobPostingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
