from openai import OpenAI
from django.conf import settings
from .scoring_service import ScoringService

class OpenAIScoringService(ScoringService):
    """
    A scoring service that uses OpenAI's GPT model to evaluate job applicants.
    """

    def __init__(self):
        """
        Initialize the OpenAI client.

        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_score(self, response):
        """
        Extract the score from the OpenAI model's response.

        Parameters:
        -----------
        response : openai.types.chat.chat_completion.ChatCompletion
            The response object from the OpenAI API call.

        Returns:
        --------
        int
            The extracted score (0-100).

        """
        content = response.choices[0].message.content
        score_line = [line for line in content.split('\n') if line.startswith('SCORE:')][0]
        return int(score_line.split(':')[1].strip())

    def _create_prompt(self, submission):
        """
        Create a prompt for the OpenAI model based on the submission.

        Parameters:
        -----------
        submission : UserSubmission
            The submission object containing the job posting and resume.

        Returns:
        --------
        str
            The formatted prompt string.
        """
        return f"""Job Description: {submission.job_posting.description}

***Resume***: {submission.resume}

Score the applicant's suitability for the job on a scale of 0-100. ***Resume*** denotes the start of the applicant's resume. Only return one score in this format: ***SCORE: 0***. Provide feedback after the score."""

    def _run_model(self, prompt):
        """
        Run the OpenAI model with the given prompt.

        Parameters:
        -----------
        prompt : str
            The formatted prompt string.

        Returns:
        --------
        openai.types.chat.chat_completion.ChatCompletion
            The response from the OpenAI model.
        """
        return self.client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who scores resumes on a scale of 0-100."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=512,
        temperature=0.6)