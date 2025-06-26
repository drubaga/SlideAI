from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion import ChatCompletionMessage
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from pydantic import BaseModel
from typing import List
from src.config import OPENAI_API_KEY, openai_model, openai_temperature, openai_max_tokens


class LLMRequest(BaseModel):
    system_prompt: str
    user_prompt: str
# not in a class 
# do readme 

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    #@retry(
     #   retry=retry_if_exception_type(Exception),
      #  wait=wait_random_exponential(min=1, max=10),
       ## stop=stop_after_attempt(3),
    #)

    #doing two things split it up get and forward messages (reforumulate function)
    def generate_response(self, request: LLMRequest) -> ChatCompletion:
        """
        Sends a prompt to OpenAI and returns the full response object.
        """
        return self.client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt}
            ],
            temperature=openai_temperature,
            max_tokens= openai_max_tokens 
        )

    def get_content(self, request: LLMRequest) -> str:
        """
        Extracts just the content from the response.
        """
        try:
            response = self.generate_response(request)
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI call failed: {e}")
