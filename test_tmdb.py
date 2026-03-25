from tmdb_utils import get_tmdb_genres, get_popular_movie_titles

print("🔹 Movie genres:")
print(get_tmdb_genres("movie"))

print("\n🔹 Popular movies:")
print(get_popular_movie_titles(3))
