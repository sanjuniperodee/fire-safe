from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StatementViewSet, StatementRequestForCompletedViewSet

router = DefaultRouter()
router.register(r'statements', StatementViewSet)
router.register(r'statement-completion-requests', StatementRequestForCompletedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]