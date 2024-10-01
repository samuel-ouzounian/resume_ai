from abc import ABC, abstractmethod

class ScoringService(ABC):
    """
    Abstract base class for scoring services.

    This class defines the interface for scoring services, ensuring that all
    concrete implementations provide the necessary methods for scoring job submissions.
    """

    def score_submission(self, submission):
        """
        Score a job application submission.

        This method orchestrates the scoring process by creating a prompt,
        running the model, and extracting the score.

        Parameters:
        -----------
        submission : UserSubmission
            The submission object containing the job posting and resume.

        Returns:
        --------
        int or float
            The calculated score for the submission.

        Note:
        -----
        This method provides a default implementation, but subclasses
        can override it if a different workflow is needed.
        """
        prompt = self._create_prompt(submission)
        output = self._run_model(prompt)
        return self.get_score(output)

    @abstractmethod
    def get_score(self, response):
        """
        Extract the score from the model's response.

        Parameters:
        -----------
        response : Any
            The response from the model. The type may vary depending on the specific model used.

        Returns:
        --------
        int or float
            The extracted score.

        Note:
        -----
        This method must be implemented by subclasses to handle the specific
        format of their model's response.
        """
        pass

    @abstractmethod
    def _create_prompt(self, submission):
        """
        Create a prompt for the model based on the submission.

        Parameters:
        -----------
        submission : UserSubmission
            The submission object containing the job posting and resume.

        Returns:
        --------
        str
            The formatted prompt string.

        Note:
        -----
        This method must be implemented by subclasses to create a prompt
        suitable for their specific model.
        """
        pass

    @abstractmethod
    def _run_model(self, prompt):
        """
        Run the model with the given prompt.

        Parameters:
        -----------
        prompt : str
            The formatted prompt string.

        Returns:
        --------
        Any
            The response from the model. The type may vary depending on the specific model used.
        Note:
        -----
        This method must be implemented by subclasses to handle the specific
        API calls or procedures for running their model.
        """
        pass