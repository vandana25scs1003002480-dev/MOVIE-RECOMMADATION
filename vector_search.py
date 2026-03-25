# vector_search.py
import chromadb
import google.generativeai as genai

EMBED_MODEL = "models/text-embedding-004"

# Create persistent vector DB
client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection("movies")

def embed(text: str):
    resp = genai.embed_content(model=EMBED_MODEL, content=text)
    return resp["embedding"]

def add_movie(movie):
    collection.add(
        ids=[str(movie["id"])],
        documents=[movie["overview"]],
        metadatas=[movie]
    )

def search_movies(query: str, n=5):
    q_vec = embed(query)
    result = collection.query(query_embeddings=[q_vec], n_results=n)
    return result["metadatas"][0]
