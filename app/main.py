from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.llm import generate_slide_content
from src.prompts.prompt_manager import PromptManager

app = FastAPI()


# Request model for the API
class SlideRequest(BaseModel):
    user_query: str  # What the user wants to generate
    text_path: str   # Path to the source .txt document


# Response model to structure the output clearly
class SlideResponse(BaseModel):
    result: str  # The generated presentation content


# Health check endpoint
@app.get("/health")
def health() -> dict:
    """
    Health check endpoint.
    Returns 200 OK if the app is running.
    """
    return {"status": "ok"}


# Main API endpoint
@app.post("/generate-slide-content", response_model=SlideResponse)
def generate_slide(req: SlideRequest) -> SlideResponse:
    """
    Generate a structured presentation from a user query and source text.
    
    Args:
        req (SlideRequest): Request body with `user_query` and `text_path`.

    Returns:
        SlideResponse: Structured result with the generated content.
    """
    try:
        # Read the content of the text file
        with open(req.text_path, "r", encoding="utf-8") as f:
            context = f.read().strip()
        
        # Build prompt using the PromptManager class
        prompt = PromptManager.build_presentation_prompt(context, req.user_query)

        # Call LLM to generate content
        response = generate_slide_content(prompt)

        # Return as structured response
        return SlideResponse(result=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
