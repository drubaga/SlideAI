from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.llm import LLMClient, LLMRequest
from src.prompts.prompt_manager import PromptManager

app = FastAPI()

# Request model for the API
class SlideRequest(BaseModel):
    user_query: str
    text_path: str

# Response model
class SlideResponse(BaseModel):
    result: str

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/generate-slide-content", response_model=SlideResponse)
def generate_slide(req: SlideRequest) -> SlideResponse:
    try:
        # Read the file content
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()

        # Build prompt using PromptManager
        prompt = PromptManager.build_presentation_prompt(context, req.user_query)

        # Create the request object for the LLM
        llm_request = LLMRequest(
            system_prompt="You are a helpful assistant generating presentation slides.",
            user_prompt=prompt
        )

        # Use the LLMClient to get the response content
        llm = LLMClient()
        response = llm.get_content(llm_request)

        return SlideResponse(result=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
