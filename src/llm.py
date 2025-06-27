from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from typing import List, Dict
from src.config import OPENAI_API_KEY, openai_model, openai_temperature, openai_max_tokens


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
    )
    def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: str = openai_model,
        **kwargs
    ):
        """
        Sends a list of messages to OpenAI and returns the full response object.

        Args:
            messages (List[Dict[str, str]]): Messages for the chat (roles: system, user, etc.)
            model (str): The LLM model to use (default: from config)
            **kwargs: Additional OpenAI parameters like temperature, max_tokens, etc.

        Returns:
            ChatCompletion: The full OpenAI response object.
        """
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

    def get_content(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """
        Extracts just the content (string) from the LLM response.

        Args:
            system_prompt (str): Instructions.
            user_prompt (str): Actual user question.
            **kwargs: Additional parameters for OpenAI (e.g. model, temperature).

        Returns:
            str: The LLM response content.
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = self.generate_response(messages=messages, **kwargs)
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI call failed: {e}")
