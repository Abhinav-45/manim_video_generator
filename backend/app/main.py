from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import animation  # Import your route
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/api/videos", StaticFiles(directory="../../outputs/videos"), name="videos")
# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes with prefix
app.include_router(animation.router, prefix="/api")
