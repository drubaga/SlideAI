from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from typing import List, Dict
from src.config import OPENAI_API_KEY, openai_model, openai_temperature, openai_max_tokens


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def _build_messages(self, system_prompt: str, user_prompt: str) -> List[Dict[str, str]]:
        """
        Builds the OpenAI messages list in the required format.
        """
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
    )
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a prompt to OpenAI and returns the full raw response.
        """
        messages = self._build_messages(system_prompt, user_prompt)
        return self.client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=openai_temperature,
            max_tokens=openai_max_tokens
        )

    def get_content(self, system_prompt: str, user_prompt: str) -> str:
        """
        Extracts just the message content from the full response.
        """
        try:
            response = self.generate_response(system_prompt, user_prompt)
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI call failed: {e}")
