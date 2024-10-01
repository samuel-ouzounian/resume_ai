from django.conf import settings
from .llama_scoring import LlamaScoringService
from .openai_scoring import OpenAIScoringService

class ScoringServiceFactory:
    """
    A factory class for creating scoring service instances.
    """

    @staticmethod
    def get_scoring_service(service_type):
        """
        Creates and returns an instance of the specified scoring service.

        Parameters:
        -----------
        service_type : str
            The type of scoring service to create. Valid options are 'openai' and 'llama'.

        Returns:
        --------
        ScoringService
            An instance of the specified scoring service.

        Raises:
        -------
        ValueError
            If an invalid service type is specified.

        Note:
        -----
        - The OpenAI service requires an API key, which is retrieved from Django settings.
        - The Llama service doesn't require additional parameters for instantiation.
        """
        services = {
            'openai': lambda: OpenAIScoringService(settings.OPENAI_API_KEY),
            'llama': LlamaScoringService
        }
        
        service_class = services.get(service_type)
        if service_class:
            return service_class()
        raise ValueError('Invalid service type specified.')