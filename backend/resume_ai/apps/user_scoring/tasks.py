from celery import shared_task
from .services.scoring_service.scoring_service_factory import ScoringServiceFactory

@shared_task
def score_submission(submission_id):
    """
    Score a user submission using the appropriate scoring service.

    This function retrieves a UserSubmission object, determines the correct
    scoring service, calculates the score, and updates the submission record.

    Parameters
    ----------
    submission_id : int
        The unique identifier of the UserSubmission to be scored.

    Returns
    -------
    float
        The calculated score for the submission.

    Raises
    ------
    UserSubmission.DoesNotExist
        If no UserSubmission with the given id exists.
    """
    from .models import UserSubmission  
    
    submission = UserSubmission.objects.get(id=submission_id)
    scoring_service = ScoringServiceFactory.get_scoring_service(submission.service)
    score = scoring_service.score_submission(submission)
    if not isinstance(score, (int, float)) or score < 0:
        raise ValueError(f"Invalid score received: {score}")
    
    submission.score = score
    submission.save()
    
    return score