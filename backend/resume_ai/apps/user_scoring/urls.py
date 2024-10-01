from django.urls import path, include
from .views.user_submission import UserSubmissionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user-submissions', UserSubmissionViewSet, basename='user-submission')
urlpatterns = [
    path('', include(router.urls)),
]