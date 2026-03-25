import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------
# Load keys
# --------------------------
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TMDB_API_KEY: raise ValueError("TMDB_API_KEY missing!")
if not GEMINI_API_KEY: raise ValueError("GEMINI_API_KEY missing!")

# Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-pro")


# --------------------------
# TMDB Helper
# --------------------------
def fetch_movies():
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
    data = requests.get(url, params=params).json()

    return [
        {
            "title": m["title"],
            "overview": m["overview"],
            "rating": m["vote_average"],
            "release": m["release_date"]
        }
        for m in data["results"]
    ]


# --------------------------
# Gemini Logic
# --------------------------
def pick_top3(mood, movie_list):
    prompt = f"""
User mood: "{mood}"

Movie list:
{movie_list}

Pick the best 3 movies for this mood.
Return only JSON:

[
  {{"title": "Movie 1", "reason": "..." }},
  {{"title": "Movie 2", "reason": "..." }},
  {{"title": "Movie 3", "reason": "..." }}
]
"""
    resp = model.generate_content(prompt)
    return resp.text


def follow_up_question(mood, top3):
    prompt = f"""
You recommended these movies for a mood of "{mood}":

{top3}

Now generate ONE smart follow-up question to refine the user's preference.
Return only the question.
"""
    resp = model.generate_content(prompt)
    return resp.text.strip()


def refine_results(mood, top3, user_pref):
    prompt = f"""
User mood: "{mood}"
User preference: "{user_pref}"

Top 3 movies:
{top3}

Pick the best 1–2 movies now.
Return JSON only:

[
  {{"title": "Movie X", "reason": "..." }},
  {{"title": "Movie Y", "reason": "..." }}
]
"""
    resp = model.generate_content(prompt)
    return resp.text.strip()


# --------------------------
# Chatbot Engine
# --------------------------
def run_chatbot():
    print("\n🎬 Welcome to MovieBot!")
    print("I recommend movies based on your mood.\n")
    print("Type 'exit' anytime to stop.\n")

    while True:
        mood = input("🤖 What mood are you in? → ")
        if mood.lower() == "exit":
            print("\n👋 See you next time!")
            break

        # Step 1: get list
        movies = fetch_movies()
        print("\n✨ Picking movies...\n")

        # Step 2: Gemini picks top 3
        top3 = pick_top3(mood, movies)
        print("🎯 Top picks:\n", top3)

        # Step 3: Ask follow-up
        q = follow_up_question(mood, top3)
        print("\n❓ " + q)
        user_pref = input("Your answer → ")

        # Step 4: Final refined list
        final = refine_results(mood, top3, user_pref)
        print("\n🍿 Final Recommendation:\n", final)

        print("\n--------------------------------------\n")


if __name__ == "__main__":
    run_chatbot()
