import openai
from src.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

"""
LLM module to interact with OpenAI's API using configurable parameters.
"""

openai.api_key = OPENAI_API_KEY

def generate_slide_content(prompt: str) -> str:
    """
    Sends a prompt to the OpenAI API and returns the generated slide content.
    Args:
        prompt (str): The prompt to send to the language model.
    Returns:
        str: The content returned by the LLM, formatted as slide content.
    Raises:
        RuntimeError: If the OpenAI API call fails.
    """

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI call fails: {e}")
