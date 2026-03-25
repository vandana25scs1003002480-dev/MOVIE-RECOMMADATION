# main.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from agent_flow import run_recommendation_agent

app = FastAPI(title="MovieMoodAgent API")


# ----------- Input model for /recommend ---------------
class UserRequest(BaseModel):
    mood: str
    media_type: str     # "movie" or "tv"
    platforms: List[str]


# ----------- Health check -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ----------- Recommendation Endpoint ------------------
@app.post("/recommend")
def recommend_movies(user: UserRequest):
    """
    Takes mood + media type + platforms and returns recommendations.
    """
    results = run_recommendation_agent(
        mood=user.mood,
        media_type=user.media_type,
        platforms=user.platforms
    )

    return {"recommendations": results}


# ----------- Start Server -----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
