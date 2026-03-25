# 🎬 MovieBot – Gemini-Powered Movie Chatbot

MovieBot is a simple Python project that uses **Google Gemini** and (optionally) **TMDB** to chat about movies and give mood-based recommendations.

Right now it has:

- `gemini_utils.py` – sanity tests for your Gemini setup (text + embeddings)
- `movie_brain.py` – the “brain” that talks to Gemini and keeps short-term memory
- `memory.py` – a tiny in-memory conversation history store
- `chatbot.py` – a console chatbot that uses `movie_brain.ask_gemini(...)`
- `movie_demo.py` *(optional)* – simple “give me 3 movies for this mood” demo using TMDB + Gemini

---

## 🧱 Project Structure

```text
ai_ml/
  .env
  .venv/                # your virtual environment (not committed)
  gemini_utils.py       # tests Gemini text + embeddings
  memory.py             # conversation memory helper
  movie_brain.py        # config + Gemini logic + memory usage
  chatbot.py            # CLI chatbot entry point
  movie_demo.py         # simple TMDB + Gemini recommender (optional)
________________________________________
🔑 Environment Variables (.env)
Create a file called .env in the project root (D:\visual studio\ai_ml) with:
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
TMDB_API_KEY=YOUR_TMDB_API_KEY_HERE   # only needed for movie_demo.py
•	GEMINI_API_KEY – from Google AI Studio
•	TMDB_API_KEY – from themoviedb.org (only used in the demo script)
No quotes, no spaces around =.
________________________________________
📦 Installation
From inside the project folder:
# 1. Activate venv (if not already)
.\.venv\Scripts\activate

# 2. Install dependencies
python -m pip install google-generativeai python-dotenv requests chromadb
chromadb is only needed later if you wire up vector search; it’s safe to install now.
________________________________________
✅ Step 1 – Test Gemini Setup
Run the utility script:
python gemini_utils.py
Expected output (shape will differ, but structure similar):
➡ Testing Gemini 2.5 Pro...
Generation OK: Hi there, I hope you're having a great day
Embedding OK — vector length: 768
If generation or embedding fails, fix this before touching the chatbot.
________________________________________
💬 Step 2 – Run the Movie Chatbot
The main chatbot entry point is chatbot.py.
python chatbot.py
You should see something like:
🎬 MovieBot (Gemini + Memory)

I can chat about movies and recommend things based on your mood.
Type 'exit' to quit.

You:
Type messages like:
•	You: recommend something thrilling but not too scary
•	You: I like sci-fi with emotional stories
•	You: suggest something funny to watch with friends
The bot will:
•	Use movie_brain.ask_gemini(...) to generate a reply
•	Use memory.py to keep a short history of the last turns so it can stay in context
Type exit, quit or bye to stop.
________________________________________
🎭 Step 3 – (Optional) Run TMDB Mood Demo
If you added movie_demo.py and set TMDB_API_KEY, you can run:
python movie_demo.py
Flow:
1.	Asks for your mood — e.g. thriller, feel-good, sad but hopeful
2.	Fetches popular movies from TMDB
3.	Uses Gemini to pick the top 3 that match your mood
4.	Prints JSON with titles + reasons
This is a good example of combining an external API (TMDB) with Gemini reasoning.
________________________________________
🧠 How movie_brain.py Works (High Level)
•	Loads .env and configures Gemini:
•	genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
•	MODEL = "models/gemini-2.5-pro"
•	Keeps a Memory() instance that stores the last few user / assistant messages.
•	ask_gemini(prompt):
o	Builds a system prompt with recent conversation context
o	Calls GenerativeModel(MODEL).generate_content(...)
o	Saves the assistant reply back into memory
o	Returns the text to chatbot.py
You can tweak the behaviour by editing the big f-string in ask_gemini() (tone, style, how strongly it focuses on movies vs general chat, etc.).
________________________________________
🧪 Troubleshooting
1. ValueError: GEMINI_API_KEY not found in your .env file
→ .env is missing, mis-named, or not in the project root.
Make sure it’s exactly ai_ml/.env and contains GEMINI_API_KEY=....
2. ModuleNotFoundError: No module named 'google.generativeai'
→ Install the SDK in the active venv:
python -m pip install google-generativeai
3. Chatbot runs but response is empty
→ Check terminal for errors from Gemini (rate limit, quota, etc.).
→ Make sure your API key is valid and not restricted.
4. TMDB demo fails
→ Check TMDB_API_KEY value in .env.
→ Confirm the key is active on themoviedb.org.
________________________________________
🧱 Next Ideas / Extensions
•	Connect this backend to a FastAPI server and call it from a Framer frontend.
•	Add vector search + ChromaDB for smarter recall of a big movie dataset.
•	Use TMDB genres and ratings to filter by:
o	mood + preferred genre (sci-fi, rom-com, etc.)
o	streaming platform
o	minimum rating / year
________________________________________
Happy hacking! 🍿
If you change file names or add new modules, remember to update this README accordingly.

