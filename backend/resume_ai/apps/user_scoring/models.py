from django.db import models
from job_postings.models import JobPosting
import uuid6

class UserSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)  # Add this line
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    resume = models.CharField(max_length=8000)
    score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"