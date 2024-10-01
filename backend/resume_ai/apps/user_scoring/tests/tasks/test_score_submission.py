import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from celery.exceptions import Retry
from user_scoring.tasks import score_submission
from user_scoring.models import UserSubmission
from user_scoring.services.scoring_service.scoring_service_factory import ScoringServiceFactory

class TestScoreSubmissionTask(TestCase):

    @patch('user_scoring.models.UserSubmission.objects.get')
    @patch('user_scoring.tasks.ScoringServiceFactory.get_scoring_service')
    def test_score_submission_success(self, mock_get_scoring_service, mock_get_submission):
        # Arrange
        mock_submission = MagicMock(spec=UserSubmission)
        mock_submission.id = 1
        mock_submission.service = 'test_service'
        mock_get_submission.return_value = mock_submission

        mock_scoring_service = MagicMock()
        mock_scoring_service.score_submission.return_value = 85.5
        mock_get_scoring_service.return_value = mock_scoring_service

        # Act
        result = score_submission(1)

        # Assert
        self.assertEqual(result, 85.5)
        mock_get_submission.assert_called_once_with(id=1)
        mock_get_scoring_service.assert_called_once_with('test_service')
        mock_scoring_service.score_submission.assert_called_once_with(mock_submission)
        mock_submission.save.assert_called_once()
        self.assertEqual(mock_submission.score, 85.5)

    @patch('user_scoring.models.UserSubmission.objects.get')
    def test_score_submission_not_found(self, mock_get_submission):
        # Arrange
        mock_get_submission.side_effect = UserSubmission.DoesNotExist

        # Act & Assert
        with self.assertRaises(UserSubmission.DoesNotExist):
            score_submission(999)

    @patch('user_scoring.models.UserSubmission.objects.get')
    @patch('user_scoring.services.scoring_service.scoring_service_factory.ScoringServiceFactory.get_scoring_service')
    def test_score_submission_scoring_error(self, mock_get_scoring_service, mock_get_submission):
        # Arrange
        mock_submission = MagicMock(spec=UserSubmission)
        mock_submission.id = 1
        mock_submission.service = 'test_service'
        mock_get_submission.return_value = mock_submission

        mock_scoring_service = MagicMock()
        mock_scoring_service.score_submission.side_effect = Exception("Scoring error")
        mock_get_scoring_service.return_value = mock_scoring_service

        # Act & Assert
        with self.assertRaises(Exception):
            score_submission(1)

    @patch('user_scoring.models.UserSubmission.objects.get')
    @patch('user_scoring.services.scoring_service.scoring_service_factory.ScoringServiceFactory.get_scoring_service')    
    def test_score_submission_invalid_score(self, mock_get_scoring_service, mock_get_submission):
        # Arrange
        mock_submission = MagicMock(spec=UserSubmission)
        mock_submission.id = 1
        mock_submission.service = 'test_service'
        mock_get_submission.return_value = mock_submission

        mock_scoring_service = MagicMock()
        mock_scoring_service.score_submission.return_value = "Invalid Score"
        mock_get_scoring_service.return_value = mock_scoring_service

        # Act & Assert
        with self.assertRaises(ValueError):
            score_submission(1)

    @patch('user_scoring.models.UserSubmission.objects.get')    
    @patch('user_scoring.services.scoring_service.scoring_service_factory.ScoringServiceFactory.get_scoring_service')    
    def test_score_submission_save_error(self, mock_get_scoring_service, mock_get_submission):
        # Arrange
        mock_submission = MagicMock(spec=UserSubmission)
        mock_submission.id = 1
        mock_submission.service = 'test_service'
        mock_submission.save.side_effect = Exception("Database error")
        mock_get_submission.return_value = mock_submission

        mock_scoring_service = MagicMock()
        mock_scoring_service.score_submission.return_value = 85.5
        mock_get_scoring_service.return_value = mock_scoring_service

        # Act & Assert
        with self.assertRaises(Exception):
            score_submission(1)

if __name__ == '__main__':
    unittest.main()