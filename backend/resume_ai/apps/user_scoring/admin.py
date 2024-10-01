from django.contrib import admin
from .models import UserSubmission
import uuid

class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'job_posting','company', 'score',  'service', 'submitted_at')
    list_filter = ('job_posting', 'service')
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(UserSubmission, UserSubmissionAdmin)