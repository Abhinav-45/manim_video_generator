Overview:
This project allows users to input a scene description (prompt), which is then interpreted by a large language model (LLM) to generate Python code using the Manim animation library. The generated code is rendered into a video and returned to the user.

Built with:
FastAPI (Backend)
React + Vite (Frontend)
Gemini (LLM for code generation and feedback)

How it Works:
-> User submits a natural language prompt describing a math/visual scene.
-> Prompt refinement system cleans and clarifies the request.
-> Gemini LLM generates Manim code based on the refined prompt.
-> Lint tool runs a feedback loop to verify code safety and correctness.
-> Final error-handling loop catches any runtime issues and re-invokes LLM if needed.
-> The valid Manim code is rendered into a video and returned to the user.

This is an experimental project built to explore natural language to animation pipelines. Contributions and feedback are welcome!
