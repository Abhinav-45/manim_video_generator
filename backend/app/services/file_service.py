# backend/app/services/file_service.py

from pathlib import Path
import shutil

# 🔥 Define correct path relative to this file
VIDEO_DIR = (Path(__file__).resolve().parent / "../../outputs/videos").resolve()

def delete_all_videos():
    print("[FileService] Looking in:", VIDEO_DIR)

    try:
        for entry in VIDEO_DIR.iterdir():
            if entry.is_file() or entry.is_symlink():
                entry.unlink()
                print(f"[FileService] Deleted file: {entry}")
            elif entry.is_dir():
                shutil.rmtree(entry)
                print(f"[FileService] Deleted folder: {entry}")
    except Exception as e:
        print(f"[FileService] Error: {e}")

