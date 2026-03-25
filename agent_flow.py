# agent_flow.py

from chroma_utils import get_or_create_collection
from gemini_utils import ask_gemini
from tmdb_utils import get_tmdb_genres

db = get_or_create_collection("movie_vectors")


def interpret_media_type(text: str) -> str:
    """Return 'movie' or 'tv' from messy user text using Gemini."""
    prompt = f"""
    A user says: "{text}".
    Decide: is it about movies or TV shows? Only reply 'movie' or 'tv'.
    """
    ans = ask_gemini(prompt).lower()
    return "tv" if "tv" in ans else "movie"


def interpret_platforms(text: str, valid_platforms: list[str]) -> list[str]:
    """Extract valid streaming platforms using Gemini."""
    prompt = f"""
    User wrote: "{text}".
    Valid platforms: {', '.join(valid_platforms)}.
    Return only exact platform names, comma separated.
    """
    raw = ask_gemini(prompt).replace("\"", "")

    out = []
    for p in raw.split(","):
        p_clean = p.strip()
        if p_clean in valid_platforms:
            out.append(p_clean)

    return out


def run_recommendation_agent(mood: str, media_type: str, platforms: list[str]):
    """
    Main engine used inside FastAPI.
    Queries vector DB and returns results filtered by:
    - mood embedding match
    - movie/tv
    - platform match
    """

    # -------- Vector Search --------
    results = db.query(
        query_texts=[mood],
        n_results=20,
        include=["documents", "metadatas"]
    )

    all_items = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        if meta["media_type"] == media_type:
            meta["overview"] = doc
            all_items.append(meta)

    # -------- Platform filter --------
    final = [
        item for item in all_items
        if any(p in item["platforms"] for p in platforms)
    ]

    return final[:5]
