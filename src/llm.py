from openai import OpenAI
from instructor import patch
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from typing import List, Dict
from src.config import OPENAI_API_KEY, openai_model
from src.models.presentation import Presentation

# Patch OpenAI client to support structured output
client = patch(OpenAI(api_key=OPENAI_API_KEY))

class LLMClient:
    """LLM client for interacting with OpenAI using structured output via Instructor."""

    def __init__(self):
        """
        Initializes the OpenAI client patched with Instructor for structured output.
        """
        self.client = client  

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
    )
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ):
        """
        Sends a chat completion request to the OpenAI API.

        Args:
            messages (List[Dict[str, str]]): List of message dicts for system/user prompts.
            **kwargs: Additional arguments for OpenAI API.

        Returns:
            OpenAI chat completion response.
        """
        return self.client.chat.completions.create(
            model=openai_model,
            messages=messages,
            **kwargs
        )

    def get_presentation(self, system_prompt: str, user_prompt: str, **kwargs) -> Presentation:
        """
        Generates a structured presentation using the OpenAI API and returns a validated Pydantic model.

        Args:
            system_prompt (str): The system-level instruction prompt.
            user_prompt (str): The user input query.
            **kwargs: Optional parameters for OpenAI API (e.g., temperature, max_tokens).

        Returns:
            Presentation: A Pydantic model containing the parsed presentation.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_model=Presentation,
                **kwargs
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to generate structured presentation: {e}")
