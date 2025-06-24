from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.llm import generate_slide_content 
from src.prompts.templates import build_prompt 

app = FastAPI()

class slideRequest(BaseModel):
    user_query: str
    text_path: str 

@app.get("/health")
def health():
    return  {"status": "ok"}

@app.post("/generate-slide-content")
def generate_slide(req: slideRequest):
    try:
        prompt = build_prompt(req.text_path, req.user_query)
        response = generate_slide_content(prompt) 
        return {"result": response}
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
