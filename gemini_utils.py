# gemini_utils.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in your .env file")

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)

# Default models (you chose option 3)
GENERATION_MODEL = "models/gemini-2.5-pro"
EMBED_MODEL      = "models/text-embedding-004"


# -----------------------------
# Basic text generation
# -----------------------------
def ask_gemini(prompt: str) -> str:
    """Generate a simple text response using Gemini 2.5 Pro."""
    try:
        model = genai.GenerativeModel(GENERATION_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini generate_content error:", e)
        return ""


# -----------------------------
# Embedding generation
# -----------------------------
def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings using models/text-embedding-004."""
    vectors = []

    try:
        for t in texts:
            resp = genai.embed_content(
                model=EMBED_MODEL,
                content=t
            )

            # Your API returns:
            # { "embedding": [...] }
            if "embedding" in resp:
                vectors.append(resp["embedding"])
            else:
                print("❌ Unexpected embedding response:", resp)
                return []

        return vectors

    except Exception as e:
        print("❌ Gemini embedding error:", e)
        return []






# -----------------------------
# Quick self-test
# -----------------------------
def test_gemini():
    """Run a quick sanity check for both text + embeddings."""
    print("➡ Testing Gemini 2.5 Pro...")
    
    # Test generation
    msg = ask_gemini("Say hello in one short friendly sentence.")
    print("Generation OK:", msg)

    # Test embeddings
    emb = embed_texts(["Hello world"])
    if emb:
        print("Embedding OK — vector length:", len(emb[0]))
    else:
        print("Embedding failed")


if __name__ == "__main__":
    test_gemini()
