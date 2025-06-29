# backend/app/routes/animation.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.master_agent import run_pipeline

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate(prompt_data: PromptRequest):
    result = run_pipeline(prompt_data.prompt)
    return result
