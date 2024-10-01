from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import JobPosting
from .serializers import JobPostingSerializer

class JobPostingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [AllowAny]