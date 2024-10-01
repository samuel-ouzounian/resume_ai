from django.test import TestCase
from django.urls import reverse
from rest_framework import status, serializers
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from user_scoring.views.user_submission import UserSubmissionViewSet
from user_scoring.models import UserSubmission
from job_postings.models import JobPosting
from user_scoring.serializers import UserSubmissionSerializer, UserSubmissionReadSerializer
from user_scoring.tasks import score_submission
from django.http import QueryDict
from rest_framework.test import APITestCase


class TestUserSubmissionViewSet(APITestCase):

    def setUp(self):
        self.list_url = reverse('user-submission-list')
        self.detail_url = reverse('user-submission-detail', kwargs={'pk': 1})

        self.client = APIClient()
    @patch('user_scoring.views.user_submission.JobPosting.objects.get')
    @patch('user_scoring.views.user_submission.UserSubmissionSerializer')
    @patch('user_scoring.views.user_submission.score_submission.delay')
    def test_create_submission_success(self, mock_score_submission, mock_serializer, mock_job_posting_get):
        # Mock the serializer to raise a validation error
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.data = {'id': 1, 'some_field': 'some_value'}        
        mock_serializer_instance.validated_data = {
                    'job_posting': MagicMock(id=1),
                    'other_field': 'value'
                }
        # Mock the score submission
        mock_task = mock_score_submission.return_value
        mock_task.id = 'mock-task-id'

        # Mock the job posting
        mock_job_posting_get.return_value = MagicMock(company="Test")

        response = self.client.post(self.list_url, {'job_posting': 1, 'other_field': 'value'})
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Submission received and scoring task started')
        self.assertEqual(response.data['task_id'], 'mock-task-id')
        self.assertIn('submission', response.data)
        mock_score_submission.assert_called_once()
        
    @patch('user_scoring.views.user_submission.UserSubmissionSerializer')
    def test_create_user_submission_invalid_data(self, mock_serializer):
        # Mock the serializer to raise a validation error
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'error': 'Invalid data'}

        # Make the POST request
        response = self.client.post(self.list_url, {'invalid': 'data'})

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid data'})

    @patch('user_scoring.views.user_submission.UserSubmissionSerializer')
    @patch('user_scoring.views.user_submission.JobPosting.objects.get')
    def test_create_user_submission_job_posting_not_found(self, mock_job_posting_get, mock_serializer):
        # Mock the serializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = {
            'job_posting': MagicMock(id=999),
            'other_field': 'value'
        }

        # Mock JobPosting.objects.get to raise a DoesNotExist exception
        mock_job_posting_get.side_effect = JobPosting.DoesNotExist

        # Make the POST request
        response = self.client.post(self.list_url, {'job_posting': 1, 'other_field': 'value'})

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Job posting not found'})

    @patch('user_scoring.views.user_submission.UserSubmissionReadSerializer')
    def test_list_submissions(self, mock_serializer):
        # Mock the serializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = [{'id': 1, 'job_posting': 1, 'other_field': 'value'}]

        # Make the GET request
        response = self.client.get(self.list_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'job_posting': 1, 'other_field': 'value'}])

    @patch('user_scoring.views.user_submission.UserSubmissionReadSerializer')
    @patch('user_scoring.views.user_submission.UserSubmissionViewSet.get_object')
    def test_get_submission(self, mock_get_object, mock_serializer):
        # Create a mock UserSubmission object
        mock_submission = MagicMock(spec=UserSubmission)
        mock_submission.id = 1
        mock_submission.job_posting_id = 1

        # Set up the mock get_object to return our mock submission
        mock_get_object.return_value = mock_submission

        # Mock the serializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.data = {'id': 1, 'job_posting': 1, 'other_field': 'value'}

        # Make the GET request
        response = self.client.get(self.detail_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'job_posting': 1, 'other_field': 'value'})

        # Verify that get_object was called
        mock_get_object.assert_called_once()


    @patch('user_scoring.views.user_submission.UserSubmissionViewSet.get_object')
    def test_get_submission_not_found(self, mock_get_object):
        # Mock get_object to raise DoesNotExist
        mock_get_object.side_effect = UserSubmission.DoesNotExist

        # Make the GET request
        response = self.client.get(self.detail_url)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Submission not found'})

if __name__ == '__main__':
    unittest.main()