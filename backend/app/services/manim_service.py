import os
import subprocess
import uuid
import platform
import shutil

OUTPUT_DIR = "outputs/videos"
SCRIPT_PATH = "outputs/temp_scene.py"

def save_code_to_file(code: str, path: str = SCRIPT_PATH):
    with open(path, "w") as f:
        f.write(code)

def render_manim_video(script_path=SCRIPT_PATH) -> str:
    """Run manim CLI to render the video and return video file path."""
    try:
        video_name = f"{uuid.uuid4().hex}.mp4"
        output_path = os.path.join(OUTPUT_DIR, video_name)

        # Ensure output dir exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Use media_dir to control base output path
        cmd = f"manim {script_path} GeneratedScene -o {video_name} -q l --media_dir outputs"

        if platform.system() == "Windows":
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)

        if result.returncode != 0:
            return f"# Manim render error:\n{result.stderr or result.stdout}"

        # Search for actual rendered video inside subdirs
        for root, dirs, files in os.walk("outputs/videos"):
            for file in files:
                if file == video_name:
                    actual_path = os.path.join(root, file)
                    shutil.move(actual_path, output_path)  # move to flat folder
                    return output_path

        return "# Rendered but video file not found."

    except Exception as e:
        return f"# Manim subprocess error: {str(e)}"
