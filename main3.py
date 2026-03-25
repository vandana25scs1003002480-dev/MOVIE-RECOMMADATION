# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from agent_flow import run_recommendation_agent


app = FastAPI(
    title="MovieMoodAgent API",
    description="Simple REST API for no-code tools like Webflow, Bubble, Framer, Wix."
)

# ------ CORS FOR NO-CODE PLATFORMS ------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or set to your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------ Input model ------
class UserRequest(BaseModel):
    mood: str
    media_type: str
    platforms: List[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend_movies(user: UserRequest):
    """
    Main endpoint your website will hit.
    """
    recs = run_recommendation_agent(
        mood=user.mood,
        media_type=user.media_type,
        platforms=user.platforms
    )

    # Ensure safe JSON for Bubble/Webflow/Wix
    cleaned = []
    for m in recs:
        cleaned.append({
            "title": m.get("title", ""),
            "overview": m.get("overview", ""),
            "poster_url": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else "",
            "platforms": m.get("platforms", []),
            "rating": m.get("vote_average", None),
            "tmdb_id": m.get("tmdb_id", ""),
            "release_date": m.get("release_date", "")
        })

    return {"results": cleaned}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
