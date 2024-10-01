import replicate
from .scoring_service import ScoringService

class LlamaScoringService(ScoringService):
    """
    A scoring service that uses the Llama model to evaluate job applicants.
    """

    
    def get_score(self, array):
        """
        Extract the score from the model's response.

        Parameters:
        -----------
        array : list
            The response array from the Llama model.

        Returns:
        --------
        int
            The extracted score.
        """
        score_index = array.index('SCORE')
        return int(array[score_index + 3])

    def _create_prompt(self, submission):
        """
        Create a prompt for the Llama model based on the submission.

        Parameters:
        -----------
        submission : UserSubmission
            The submission object containing the job posting and resume.

        Returns:
        --------
        str
            The formatted prompt string.
        """
        return f"Job Description: {submission.job_posting.description}\n\n***Resume***: {submission.resume}\n\nScore the applicant's suitability for the job on a scale of 0-100. ***Resume*** denotes the start of the applicants resume. Only return one score in this format: ***SCORE: 0***. Provide feedback after the score."

    def _run_model(self, prompt):
        """
        Run the Llama model with the given prompt.

        Parameters:
        -----------
        prompt : str
            The formatted prompt string.

        Returns:
        --------
        list
            The response from the Llama model.
        """
        return replicate.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                "top_k": 0,
                "top_p": 0.9,
                "prompt": prompt,
                "max_tokens": 512,
                "min_tokens": 0,
                "temperature": 0.6,
                "system_prompt": "You are a helpful assistant who scores resumes on a scale of 0-100.",
                "length_penalty": 0.5,
                "stop_sequences": "<|end_of_text|>,<|eot_id|>",
                "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                "presence_penalty": 1.15,
                "log_performance_metrics": False
            })