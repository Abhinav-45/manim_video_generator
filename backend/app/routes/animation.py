# backend/app/routes/animation.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_manim_code
from app.services.manim_service import save_code_to_file, render_manim_video
from pathlib import Path

# from backend.app.services import refine_prompt
# from backend.app.services.file_service import delete_all_videos
from app.services.file_service import delete_all_videos
from app.services.refine_prompt import refine_prompt

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate(prompt_data: PromptRequest):
    raw_prompt = prompt_data.prompt
    print("[Animation] Calling delete_all_videos()")

    delete_all_videos()
    

    refined_prompt = refine_prompt(raw_prompt)

    # Step 1: Get Manim code from Gemini
    manim_code = generate_manim_code(refined_prompt)

    if manim_code.startswith("# Error"):
        return {"status": "error", "message": manim_code}

    # Step 2: Save code to file
    save_code_to_file(manim_code)

    # Step 3: Render Manim scene
    video_path = render_manim_video()

    if video_path.startswith("#"):
        return {"status": "error", "message": video_path}

    return {
    "status": "success",
    "video_path": Path(video_path).name  # just return filename
}

