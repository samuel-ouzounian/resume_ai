from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user_scoring.models import UserSubmission
from job_postings.models import JobPosting 
from user_scoring.tasks import score_submission
from user_scoring.serializers import UserSubmissionSerializer, UserSubmissionReadSerializer

class UserSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle user submissions for job postings.
    """
    queryset = UserSubmission.objects.all()
    serializer_class = UserSubmissionSerializer

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return UserSubmissionSerializer
        return UserSubmissionReadSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new user submission and initiate the scoring task.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                # Retrieve the associated job posting
                job_posting = JobPosting.objects.get(id=serializer.validated_data['job_posting'].id)
                
                # Create the submission
                submission = serializer.save(company=job_posting.company)

                # Initiate the scoring task asynchronously
                task = score_submission.delay(submission.id)
                
                # Prepare the response data
                response_data = {
                    'message': 'Submission received and scoring task started',
                    'task_id': task.id,
                    'submission': UserSubmissionSerializer(submission).data
                }
                print(response_data)
                return Response(response_data, status=status.HTTP_201_CREATED)
            except JobPosting.DoesNotExist:
                return Response({'error': 'Job posting not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific user submission.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except UserSubmission.DoesNotExist:
            return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)