from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.applications.views import ApplicationViewSet, ApplicationReviewView

router = DefaultRouter()

router.register(r'', ApplicationViewSet, basename='applications')

urlpatterns = [
    path('<uuid:id>/review/', ApplicationReviewView.as_view(), name='application-review')
] + router.urls