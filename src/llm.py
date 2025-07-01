from openai import OpenAI
from instructor import patch
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from typing import List, Dict
from src.config import OPENAI_API_KEY, openai_model
from src.models.presentation import Presentation

# Patch OpenAI client to support structured output
client = patch(OpenAI(api_key=OPENAI_API_KEY))

class LLMClient:
    def __init__(self):
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
        return self.client.chat.completions.create(
            model=openai_model,
            messages=messages,
            **kwargs
        )

    def get_presentation(self, system_prompt: str, user_prompt: str, **kwargs) -> Presentation:
        try:
            # Call OpenAI with structured output directly
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_model=Presentation,  # this works because of instructor
                **kwargs
            )
            return response  # This is already parsed as a Presentation Pydantic model
        except Exception as e:
            raise RuntimeError(f"Failed to generate structured presentation: {e}")
