from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.llm import LLMClient
from src.prompts.prompt_manager import PromptManager
from src.config import openai_model, openai_temperature, openai_max_tokens
from src.models.presentation import Presentation
from src.pptx_generator.builder import PPTXBuilder
from typing import Optional
import os

from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app instance
app = FastAPI()


# Request model containing user prompt and path to the input text file
class SlideRequest(BaseModel):
    user_query: str
    text_path: str
    enable_images: bool = False
    image_provider: Optional[str] = None
    template: Optional[str] = "default"  

@app.get("/health")
def health() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: A simple response to verify the backend is running.
    """
    return {"status": "ok"}


@app.post("/generate-slide-content", response_model=Presentation)
def generate_slide(req: SlideRequest) -> Presentation:
    """
    Generates structured slide content from a user prompt and input text file.

    Args:
        req (SlideRequest): Contains user input and .txt file path.

    Returns:
        Presentation: A structured presentation object, including slide titles,
                      bullet points, key messages, and optional image keywords.
    """
    try:
        # Read context from the input .txt file
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()

        # Construct system and user prompts
        system_prompt = PromptManager.get_system_prompt(context)
        user_prompt = req.user_query

        # Call LLM to generate structured presentation content
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


@app.post("/generate-pptx-from-template")
def generate_pptx_with_template(presentation: Presentation):
    """
    Generates a PowerPoint (.pptx) file from a structured Presentation object.

    Args:
        presentation (Presentation): Structured content including slides and images.

    Returns:
        FileResponse: Downloadable .pptx file generated using a predefined template.
    """
    try:
        # Use OOP builder to generate the .pptx file
        pptx_path = PPTXBuilder(presentation).build()
        return FileResponse(
            pptx_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=os.path.basename(pptx_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-pptx")
def generate_pptx_from_prompt(req: SlideRequest):
    """
    Generates a PowerPoint (.pptx) presentation from a user prompt and a context file.

    Reads the context from the given text path, creates a prompt for the LLM,
    generates slide content, and builds a presentation. Optionally includes images
    based on user preferences.

    Args:
        req (SlideRequest): Includes the context file path, user prompt, image flag, and provider.

    Returns:
        FileResponse: The generated .pptx file.

    Raises:
        HTTPException: If an error occurs during generation or file creation.
    """
    try:
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()

        system_prompt = PromptManager.get_system_prompt(context)
        user_prompt = req.user_query

        llm = LLMClient()
        presentation = llm.get_presentation(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=openai_model,
            temperature=openai_temperature,
            max_tokens=openai_max_tokens
        )
        presentation.template = req.template  

        # Inject user's image preferences directly into builder
        pptx_path = PPTXBuilder(
            presentation=presentation,
            enable_images=req.enable_images,
            image_provider=req.image_provider
        ).build()


        return FileResponse(
            pptx_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=os.path.basename(pptx_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

