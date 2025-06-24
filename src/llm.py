import openai 
from src.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_slide_content(prompt: str) -> str:
    try:
        response=openai.ChatCompletion.create(
            model="gpt-4",
            messages= [{"role":"user", "content": prompt}],
            temperature = 0.1,
            max_tokens = 1500
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI call dailes: {e}")