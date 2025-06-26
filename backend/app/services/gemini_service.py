 # backend/app/services/gemini_service.py

from dotenv import load_dotenv
import os

load_dotenv()  # 👈 loads from .env file
api_key = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai
genai.configure(api_key=api_key)

def clean_code_block(code: str) -> str:
    """Remove triple quotes or markdown-style code fencing from Gemini output."""
    lines = code.strip().splitlines()

    # Remove leading and trailing triple quotes or ```python
    if lines[0].strip().startswith("'''") or lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and (lines[-1].strip().endswith("'''") or lines[-1].strip().endswith("```")):
        lines = lines[:-1]

    return "\n".join(lines)



def generate_manim_code(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemma-3-27b-it")
        response = model.generate_content(
            f"""You're a Python developer using Manim.
Generate a full Manim script based on: "{prompt}".
Rules:
- Use `from manim import *`
- Define a class `GeneratedScene(Scene)`
- No markdown formatting — only return raw Python code.
"""
        )
        raw_code = response.text
        return clean_code_block(raw_code)  # 🧼 Clean before returning
    except Exception as e:
        return f"# Error generating code: {e}"
