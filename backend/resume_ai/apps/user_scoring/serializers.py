from rest_framework import serializers
from .models import UserSubmission
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone

class UserSubmissionSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    days_since_submission = serializers.SerializerMethodField()

    class Meta:
        model = UserSubmission
        fields = ['id', 'job_posting', 'first_name', 'last_name', 'email', 'phone_number', 'resume', 'score', 'submitted_at', 'service', 'full_name', 'days_since_submission']
        read_only_fields = ['score', 'submitted_at', 'id']

    def validate_email(self, value):
        validator = EmailValidator(message="Enter a valid email address.")
        validator(value)
        return value

    def validate_phone_number(self, value):
        validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
        validator(value)
        return value

    def validate(self, data):
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            raise serializers.ValidationError("First name and last name must be at least 2 characters long.")
        return data

    def create(self, validated_data):
        validated_data['submitted_at'] = timezone.now()
        return UserSubmission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_days_since_submission(self, obj):
        if obj.submitted_at:
            return (timezone.now() - obj.submitted_at).days
        return None

class UserSubmissionReadSerializer(UserSubmissionSerializer):
    class Meta(UserSubmissionSerializer.Meta):
        fields = ['id', 'job_posting', 'company', 'full_name', 'email', 'score', 'submitted_at', 'days_since_submission']