# main.py

from gemini_utils import test_gemini
from tmdb_utils import get_tmdb_genres, discover_by_genre_and_platform

if __name__ == "__main__":
    print("\nTesting Gemini…")
    test_gemini()

    print("\nMovie genres:", get_tmdb_genres("movie"))
