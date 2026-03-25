# movie_brain.py
import os                      # ✅ add this
from dotenv import load_dotenv # ✅ and this
import google.generativeai as genai
from memory import Memory
from vector_search import search_movies

# load .env
load_dotenv()

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "models/gemini-2.5-pro"

memory = Memory()

def ask_gemini(prompt):
    context = memory.get_summary()
    full_prompt = f"""
You are MovieBot, an intelligent movie recommendation agent.
Here is the conversation so far:

{context}

User request:
{prompt}

Respond naturally and ask follow-up questions when needed.
"""
    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content(full_prompt)
    memory.add("assistant", resp.text)
    return resp.text

