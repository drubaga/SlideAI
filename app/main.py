from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.llm import LLMClient
from src.prompts.prompt_manager import PromptManager
from src.config import openai_model, openai_temperature, openai_max_tokens
from src.models.presentation import Presentation

app = FastAPI()


class SlideRequest(BaseModel):
    """Request model containing the user query and path to the input text file."""
    user_query: str
    text_path: str


@app.get("/health")
def health() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: A simple status message indicating the app is running.
    """
    return {"status": "ok"}


@app.post("/generate-slide-content", response_model=Presentation)
def generate_slide(req: SlideRequest) -> Presentation:
    """
    Generates a structured slide presentation from a user query and source text.

    Args:
        req (SlideRequest): Contains user prompt and path to the .txt file.

    Returns:
        Presentation: A structured presentation object based on the prompts.

    Raises:
        HTTPException: If file reading or LLM generation fails.
    """
    try:
        # Load file content from path
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()

        # Compose prompts
        system_prompt = PromptManager.get_system_prompt(context)
        user_prompt = req.user_query

        # Generate structured output using Pydantic model
        llm = LLMClient()
        presentation = llm.get_presentation(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=openai_model,
            temperature=openai_temperature,
            max_tokens=openai_max_tokens
        )
        return presentation

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
