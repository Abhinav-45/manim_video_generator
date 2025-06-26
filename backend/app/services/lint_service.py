import subprocess

def lint_code(code: str) -> dict:
    temp_path = "outputs/temp_scene.py"
    with open(temp_path, "w") as f:
        f.write(code)

    # Dry-run Manim
    manim_proc = subprocess.run(
        ["manim", temp_path, "GeneratedScene", "-ql", "--dry_run"],
        capture_output=True,
        text=True
    )

    # Ruff check
    ruff_proc = subprocess.run(
        ["ruff", temp_path],
        capture_output=True,
        text=True
    )

    has_errors = manim_proc.returncode != 0 or ruff_proc.returncode != 0

    return {
        "has_errors": has_errors,
        "manim_output": manim_proc.stderr + manim_proc.stdout,
        "ruff_output": ruff_proc.stdout
    }
