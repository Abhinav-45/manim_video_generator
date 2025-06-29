# app/services/master_agent.py

from pathlib import Path
from app.services.refine_prompt import refine_prompt
from app.services.gemini_service import (
    generate_manim_code,
    refine_code_with_feedback,
    refine_code_with_render_error,  # NEW: for render errors
)
from app.services.manim_service import save_code_to_file, render_manim_video
from app.services.file_service import delete_all_videos
from app.services.lint_service import lint_code

MAX_RETRIES = 3  # Lint retry loop
FINAL_RENDER_RETRY = True  # One retry if render fails

def run_pipeline(raw_prompt: str):
    delete_all_videos()

    # Step 1: Refine user prompt
    refined_prompt = refine_prompt(raw_prompt)
    print("[MasterAgent] Refined Prompt:", refined_prompt)

    # Step 2: Generate code from Gemini
    manim_code = generate_manim_code(refined_prompt)
    print("[MasterAgent] Initial code generated.")

    if manim_code.startswith("# Error"):
        return {"status": "error", "message": "Failed to generate code from Gemini."}

    # Step 3: Lint + Feedback Loop
    for attempt in range(MAX_RETRIES):
        lint_result = lint_code(manim_code)
        if lint_result["success"]:
            print(f"[MasterAgent] Lint passed on attempt {attempt + 1}")
            break
        print(f"[MasterAgent] Lint failed on attempt {attempt + 1}. Fixing...")
        manim_code = refine_code_with_feedback(
            original_prompt=refined_prompt,
            broken_code=manim_code,
            lint_errors=lint_result["errors"]
        )
    else:
        return {
            "status": "error",
            "message": f"Linting failed after {MAX_RETRIES} retries."
        }

    # Step 4: Save and Render
    save_code_to_file(manim_code)
    print("[MasterAgent] Code saved. Starting render...")

    success, result = render_manim_video()
    if success:
        return {
            "status": "success",
            "video_path": Path(result).name
        }

    print("[MasterAgent] Initial render failed. Trying fix with render feedback...")

    # Step 5: Optional final attempt to fix rendering
    if FINAL_RENDER_RETRY:
        manim_code = refine_code_with_render_error(manim_code, result)
        lint_result = lint_code(manim_code)

        if lint_result["success"]:
            save_code_to_file(manim_code)
            success, result = render_manim_video()
            if success:
                return {
                    "status": "success",
                    "video_path": Path(result).name
                }

    # Final failure
    return {
        "status": "error",
        "message": f"Rendering failed. Details:\n{result}"
    }
