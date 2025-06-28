# backend/app/services/refiner_service.py

def refine_prompt(raw_prompt: str) -> str:
    """
    Refines the input prompt to make it clearer and more suitable for generating Manim code.
    Keeps the complexity low.
    """
    raw_prompt = raw_prompt.strip()

    # Handle empty input
    if not raw_prompt:
        return "Show a simple title that says 'Welcome to Manim'."

    # Basic heuristic rules
    refinements = [
    ("graph", "Create a simple graph with labeled axes."),
    ("plot", "Plot a basic mathematical function like y = x^2."),
    ("circle", "Draw a circle and label its radius."),
    ("square", "Draw a square and label its sides."),
    ("triangle", "Draw a triangle and mark its angles."),
    ("rectangle", "Draw a rectangle and show its length and width."),
    ("equation", "Write and transform a simple math equation."),
    ("formula", "Display a math formula using Tex."),
    ("title", "Show a centered title with fade-in animation."),
    ("list", "Display a bullet-point list using Tex."),
    ("text", "Display centered text with basic animation."),
    ("welcome", "Show a welcome message with simple animation."),
    ("rotate", "Rotate a shape like a square or triangle."),
    ("scale", "Scale a basic shape and animate the transformation."),
    ("move", "Move an object from left to right."),
    ("highlight", "Highlight a part of a diagram or equation."),
    ("matrix", "Display a 2x2 matrix using MathTex."),
    ("arrow", "Draw an arrow pointing from one object to another."),
    ("number line", "Show a number line from -5 to 5."),
    ("coordinate", "Draw a coordinate plane and label the axes."),
    ("label", "Add labels to shapes or points."),
    ("transform", "Transform one shape into another."),
    ("animate", "Animate a basic shape using fade-in and movement."),
    ("scene", "Create a simple Manim scene with one shape and animation."),
    ("diagram", "Draw a basic labeled diagram using lines and shapes."),
    ("bar chart", "Create a bar chart with 3 categories."),
    ("line chart", "Draw a line chart showing trend over time."),
    ("text animation", "Animate the writing of a short sentence."),
    ("introduction", "Show a simple animated introduction text."),
    ("transform", "Fade out the old object before creating new object")
]


    for keyword, replacement in refinements:
        if keyword in raw_prompt.lower():
            return f"{replacement} Based on user request: '{raw_prompt}'."

    # Default fallback if no keyword matches
    return f"Create a basic scene that illustrates: '{raw_prompt}' using simple Manim elements."

