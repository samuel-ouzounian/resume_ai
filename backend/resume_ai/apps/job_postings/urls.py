from .views import JobPostingViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', JobPostingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]