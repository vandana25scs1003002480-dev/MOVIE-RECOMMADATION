import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# Load ENV
# -------------------------------
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY missing")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-pro")


# -------------------------------
# TMDB Fetch
# -------------------------------
def search_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}

    data = requests.get(url, params=params).json()

    movies = [
        {
            "title": m["title"],
            "overview": m["overview"],
            "rating": m["vote_average"],
            "release": m["release_date"]
        }
        for m in data["results"]
    ]

    return movies


# -------------------------------
# Gemini picks first 3 movies
# -------------------------------
def pick_initial(mood, movies):
    prompt = f"""
User mood: "{mood}"

Movie list:
{movies}

Pick the best 3 movies for this mood.
Return strictly in JSON:

[
  {{"title": "Movie 1", "reason": "..." }},
  {{"title": "Movie 2", "reason": "..." }},
  {{"title": "Movie 3", "reason": "..." }}
]
"""
    resp = model.generate_content(prompt)
    return resp.text


# -------------------------------
# Gemini follow-up question
# -------------------------------
def ask_follow_up(mood, top3_list):
    prompt = f"""
You recommended these movies for a mood of "{mood}":

{top3_list}

Now generate ONE follow-up question that helps refine the user’s taste.
Examples:
- “Do you prefer something fast-paced or slow and emotional?”
- “Do you want a dark tone or something more fun?”

Return ONLY the question text.
"""

    resp = model.generate_content(prompt)
    return resp.text.strip()


# -------------------------------
# Refine with user preference
# -------------------------------
def refine_recommendation(mood, top3_list, user_preference):
    prompt = f"""
User mood: "{mood}"
User preference from follow-up: "{user_preference}"

Your earlier top picks:
{top3_list}

Now pick the **best 1 or 2 movies** based on mood + preference.
Return JSON:

[
  {{"title": "Movie X", "reason": "..." }},
  {{"title": "Movie Y", "reason": "..." }}
]
"""

    resp = model.generate_content(prompt)
    return resp.text.strip()


# -------------------------------
# Main App
# -------------------------------
if __name__ == "__main__":
    print("\n🎬 Smart Movie Recommender\n")

    mood = input("What mood are you in? → ")

    movies = search_movies()
    print("\n✨ Choosing best matches...\n")

    first_pick = pick_initial(mood, movies)
    print("Top 3 picks:")
    print(first_pick)

    print("\n🤖 Gemini follow-up question:\n")
    follow_q = ask_follow_up(mood, first_pick)
    print(follow_q)

    user_pref = input("\nYour answer → ")

    final = refine_recommendation(mood, first_pick, user_pref)

    print("\n🎯 Final Recommendation:\n")
    print(final)
