from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmitHistoryViewSet

router = DefaultRouter()
router.register(r"submit_history", SubmitHistoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
