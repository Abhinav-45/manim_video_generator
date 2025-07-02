from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import animation  
from fastapi.staticfiles import StaticFiles
app = FastAPI()
from pathlib import Path
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent  
VIDEO_DIR = BASE_DIR / "outputs" / "videos"

app.mount("/api/videos", StaticFiles(directory=str(VIDEO_DIR)), name="videos")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(animation.router, prefix="/api")
