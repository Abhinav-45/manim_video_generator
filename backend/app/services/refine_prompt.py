import re

COLOR_MAP = {
    "red": "#e07a5f",
    "blue": "#525893",
    "green": "#87c2a5",
    "black": "#343434",
    "white": "#ffffff",
    "yellow": "#f4d35e",
    "purple": "#9b5de5",
    "orange": "#f8961e",
    "brown": "#a0522d",
    "pink": "#ff69b4",
    "gray": "#808080",
    "grey": "#808080",
    "cyan": "#00ffff",
    "magenta": "#ff00ff"
}

def replace_named_colors_with_hex(prompt: str) -> str:
    def color_replacer(match):
        color = match.group(1).lower()
        return COLOR_MAP.get(color, color)  # fallback to original if unknown

    return re.sub(r'\b(' + '|'.join(COLOR_MAP.keys()) + r')\b', color_replacer, prompt, flags=re.IGNORECASE)


def is_transformation_request(prompt: str) -> bool:
    indicators = [
        "transform", "morph", "change into", "becomes", "turns into",
        "point to", "circle to", "square to", "convert", "→", "->", "into a", "to a"
    ]
    return any(indicator in prompt.lower() for indicator in indicators)


def extract_transformation_sequence(prompt: str) -> list:
    """Extract transformation sequence of any length from the prompt."""
    prompt_lower = prompt.lower()
    
    # Define separators for different transformation syntax
    separators = [
        (r'\s+to\s+', ' to '),
        (r'\s*→\s*', '→'),
        (r'\s*->\s*', '->'),
        (r'\s+into\s+', ' into '),
        (r'\s+becomes\s+', ' becomes '),
        (r'\s+transforms?\s+to\s+', ' transforms to '),
        (r'\s+morphs?\s+to\s+', ' morphs to '),
        (r'\s+changes?\s+into\s+', ' changes into ')
    ]
    
    # Try each separator type
    for sep_pattern, sep_display in separators:
        # Split by the separator and clean up
        parts = re.split(sep_pattern, prompt_lower)
        if len(parts) > 1:
            # Clean each part - extract just the shape/object name
            sequence = []
            for part in parts:
                # Remove common prefixes/suffixes and extra words
                cleaned = re.sub(r'\b(a|an|the|from|change|transform|morph)\b', '', part.strip())
                cleaned = re.sub(r'\b(transformation|into|to)\b.*', '', cleaned).strip()
                
                # Extract the main object/shape name (first meaningful word)
                words = cleaned.split()
                if words:
                    # Take the first word that looks like a shape/object
                    for word in words:
                        if len(word) > 1 and word.isalpha():
                            sequence.append(word)
                            break
            
            if len(sequence) > 1:
                return sequence
    
    # Fallback: try to find individual transformation pairs and chain them
    transformation_pairs = []
    
    # Look for patterns like "X to Y" throughout the text
    pair_patterns = [
        r'\b(\w+)\s+to\s+(\w+)\b',
        r'\b(\w+)\s*→\s*(\w+)\b',
        r'\b(\w+)\s*->\s*(\w+)\b',
        r'\b(\w+)\s+into\s+(\w+)\b',
        r'\b(\w+)\s+becomes\s+(\w+)\b'
    ]
    
    for pattern in pair_patterns:
        matches = re.findall(pattern, prompt_lower)
        for match in matches:
            transformation_pairs.append(list(match))
    
    # If we found pairs, try to chain them into a sequence
    if transformation_pairs:
        # Start with the first pair
        sequence = list(transformation_pairs[0])
        used_pairs = {0}
        
        # Try to extend the sequence by finding connecting pairs
        while True:
            extended = False
            for i, pair in enumerate(transformation_pairs):
                if i in used_pairs:
                    continue
                
                # Check if this pair extends our sequence
                if pair[0] == sequence[-1]:  # pair starts where sequence ends
                    sequence.append(pair[1])
                    used_pairs.add(i)
                    extended = True
                    break
                elif pair[1] == sequence[0]:  # pair ends where sequence starts
                    sequence.insert(0, pair[0])
                    used_pairs.add(i)
                    extended = True
                    break
            
            if not extended:
                break
        
        return sequence
    
    return []


def match_keywords(prompt: str, rules: list) -> str:
    prompt_lower = prompt.lower()
    for keywords, refinement in rules:
        if any(keyword in prompt_lower for keyword in keywords):
            return f"{refinement}. Based on user request: '{prompt}'."
    return None


def refine_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    if not prompt:
        return "Show a simple title that says 'Welcome to Manim'."

    # Replace named colors with hex values
    prompt = replace_named_colors_with_hex(prompt)

    # 1. Enhanced transformation logic - now handles any number of transformations
    if is_transformation_request(prompt):
        sequence = extract_transformation_sequence(prompt)
        print(f"DEBUG: Detected transformation sequence: {sequence}")  # Debug line
        
        if len(sequence) >= 4:
            # Handle 4+ step transformations
            steps = " → ".join(sequence)
            return f"Create a complex animated transformation sequence: {steps}. Use Manim objects and chained Transform animations with appropriate timing delays between each step. Also fade out the former object while creating the latter object "
        elif len(sequence) == 3:
            return f"Create a smooth animated transformation sequence: {sequence[0]} transforms to {sequence[1]} which then transforms to {sequence[2]}. Use Manim objects (Circle, Square, Triangle, etc.) and Transform animations with proper timing."
        elif len(sequence) == 2:
            return f"Create a smooth animated transformation: {sequence[0]} transforms into {sequence[1]}. Use appropriate Manim shapes and Transform animation with smooth transitions."
        else:
            # If we detected transformation keywords but couldn't extract sequence
            return f"Create an animated transformation scene based on: '{prompt}'. Use Manim Transform animations between appropriate geometric shapes."

    # 2. Rule categories (rest of the code remains the same)
    educational_rules = [
        (["explain", "how", "why", "process", "step by step", "procedure"], 
         "Create a step-by-step educational animation explaining the concept with clear visual progression"),
        
        (["prove", "proof", "theorem", "lemma", "show that"], 
         "Create an animated mathematical proof with step-by-step derivations using MathTex"),
        
        (["solve", "solution", "solving", "find", "calculate"], 
         "Animate the solving process step-by-step showing each mathematical operation"),
        
        (["method", "algorithm", "technique", "approach"], 
         "Demonstrate the method with animated steps and visual examples"),
        
        (["concept", "definition", "principle", "theory"], 
         "Illustrate the concept with visual examples and clear explanations"),
        
        (["derive", "derivation", "from", "starting"], 
         "Show the mathematical derivation process with animated equation transformations"),
        
        (["compare", "difference", "versus", "vs", "contrast"], 
         "Create a side-by-side comparison animation highlighting key differences"),
        
        (["example", "demonstrate", "illustration", "show"], 
         "Provide an animated example with clear visual demonstration")
    ]

    math_rules = [
        (["quadratic", "parabola", "ax²"], "Animate quadratic functions and their properties with graphing"),
        (["limit", "approaches", "infinity"], "Visualize limits with animated approaching values"),
        (["integration", "area under curve"], "Show integration as area calculation with animated filling"),
        (["differentiation", "slope", "tangent"], "Animate derivatives as changing slopes with tangent lines"),
        (["trigonometry", "sin", "cos", "tan"], "Create animated trigonometric visualizations with unit circle"),
        (["vector", "dot product", "cross product"], "Animate vector operations in 2D/3D space"),
        (["series", "sequence", "convergence"], "Show series convergence with animated partial sums"),
        (["equation", "solve", "algebra"], "Display and animate mathematical equation solving"),
        (["formula", "expression"], "Show formula using MathTex with step-by-step breakdown"),
        (["function", "plot", "graph"], "Plot mathematical function with animated axes and curve"),
        (["matrix", "determinant", "linear"], "Display matrix operations with animated transformations")
    ]

    animation_rules = [
        (["animate", "moving", "move"], "Create an animated scene with smooth movement transitions"),
        (["rotate", "rotation", "spin"], "Animate rotation with proper timing and easing"),
        (["scale", "scaling", "grow", "shrink", "resize"], "Animate scaling with smooth size changes"),
        (["fade", "appear", "disappear"], "Create fade animations with proper opacity transitions"),
        (["slide", "glide", "translate"], "Animate objects moving across screen with smooth paths")
    ]

    visual_rules = [
        (["diagram", "flowchart", "chart"], "Create an educational diagram with clear labels and connections"),
        (["timeline", "history", "chronology"], "Show a timeline with animated progression of events"),
        (["cycle", "process flow", "workflow"], "Animate a cyclical process with connected steps"),
        (["structure", "anatomy", "breakdown"], "Create a structural breakdown with animated components"),
        (["comparison table", "pros and cons"], "Display comparison with animated reveal of points")
    ]

    shape_rules = [
        (["circle"], "Draw an animated circle with properties"),
        (["square"], "Draw an animated square with transformations"),
        (["triangle"], "Draw an animated triangle"),
        (["rectangle"], "Draw an animated rectangle"),
        (["line"], "Draw an animated line"),
        (["arrow"], "Draw animated arrows for emphasis")
    ]
    
    text_rules = [
        (["title", "heading"], "Display animated title with emphasis effects"),
        (["text", "write", "display"], "Show text with typewriter or fade-in animation"),
        (["list", "bullet"], "Display animated bullet-point list with sequential reveals"),
        (["welcome", "introduction"], "Create engaging welcome screen with animations")
    ]

    for category in [educational_rules, math_rules, visual_rules, animation_rules, shape_rules, text_rules]:
        result = match_keywords(prompt, category)
        if result:
            return result

    if any(word in prompt.lower() for word in ["learn", "teach", "understand", "knowledge", "study", "lesson"]):
        return f"Create an educational Manim animation that teaches: '{prompt}' with clear visual explanations and step-by-step progression."

    return f"Create an animated Manim scene that illustrates: '{prompt}' using appropriate visual elements and smooth animations."

