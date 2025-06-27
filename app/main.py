from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.llm import LLMClient
from src.prompts.prompt_manager import PromptManager
from src.config import openai_model, openai_temperature, openai_max_tokens

app = FastAPI()

class SlideRequest(BaseModel):
    user_query: str
    text_path: str

class SlideResponse(BaseModel):
    result: str

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/generate-slide-content", response_model=SlideResponse)
def generate_slide(req: SlideRequest) -> SlideResponse:
    try:
        # Load file content
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()

        # Get prompts
        system_prompt = PromptManager.get_system_prompt(context)
        user_prompt = req.user_query

        # Use updated LLMClient
        llm = LLMClient()
        response = llm.get_content( system_prompt, user_prompt, model=openai_model, temperature=openai_temperature, max_tokens=openai_max_tokens)
        return SlideResponse(result=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
