from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from typing import List, Dict
import json

from src.config import OPENAI_API_KEY, openai_model, openai_temperature, openai_max_tokens
from src.models.presentation import Presentation  


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
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )

    def get_presentation(self, system_prompt: str, user_prompt: str, **kwargs) -> Presentation:
        """
        Sends prompt to OpenAI and parses the structured response into a validated Presentation model.
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            response = self.generate_response(messages=messages, **kwargs)
            content = response.choices[0].message.content.strip()
    

            parsed_json = json.loads(content)
            return Presentation(**parsed_json)
        except Exception as e:
            raise RuntimeError(f"Failed to generate structured presentation: {e}")
