from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def clean_code_block(code: str) -> str:
    """Remove triple quotes or markdown-style code fencing from Gemini output."""
    lines = code.strip().splitlines()

    if lines and (lines[0].strip().startswith("'''") or lines[0].strip().startswith("```")):
        lines = lines[1:]
    if lines and (lines[-1].strip().endswith("'''") or lines[-1].strip().endswith("```")):
        lines = lines[:-1]

    return "\n".join(lines)

def generate_manim_code(prompt: str) -> str:
    """Generate Manim Python code from a refined user prompt."""
    try:
        response = model.generate_content(
            f"""You're a Python developer using Manim.
Generate a full Manim script based on: "{prompt}".
Rules:
- Use `from manim import *`
- Define a class `GeneratedScene(Scene)`
- No markdown formatting — only return raw Python code.
"""
        )
        print(model)
        raw_code = response.text
        return clean_code_block(raw_code)
    except Exception as e:
        return f"# Error generating code: {e}"

def refine_code_with_feedback(original_prompt: str, broken_code: str, lint_errors: str) -> str:
    """Refine Manim code based on lint errors using Gemini."""
    try:
        response = model.generate_content(
            f"""You're a Python and Manim expert. The following code has issues detected by a Python linter.

Your task is to fix the code so it:
- Passes linting (fixes all syntax and style errors)
- Fulfills the user's original intent
- Remains minimal and readable
- Uses proper Manim imports and syntax

---

User Prompt: {original_prompt}

Linting Errors: {lint_errors}

Broken Code: {broken_code}

---

Return only the corrected Manim Python code. Do not include any explanations or markdown."""
        )
        fixed_code = response.text
        return clean_code_block(fixed_code)
    except Exception as e:
        print(f"Error in refine_code_with_feedback: {e}")
        return broken_code  # Return original code if refinement fails

def refine_code_with_render_error(broken_code: str, render_error: str) -> str:
    prompt = f"""
You are an expert Python and Manim developer. The following Manim code failed during rendering. Fix the code based on the rendering error below.

Ensure:
- A class `GeneratedScene` exists and inherits from `Scene`.
- All colors and objects used are valid in Manim.
- Runtime syntax issues are resolved.

--- CODE ---
{broken_code}

--- RENDER ERROR ---
{render_error}

Return only the corrected Manim code.
"""
    return generate_manim_code(prompt)
