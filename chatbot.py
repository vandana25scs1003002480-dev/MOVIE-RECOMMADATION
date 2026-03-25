# chatbot.py

from movie_brain import ask_gemini  # ✅ only import this


def run():
    print("\n🎬 MovieBot (Gemini + Memory)\n")
    print("I can chat about movies and recommend things based on your mood.")
    print("Type 'exit' to quit.\n")

    while True:
        user_msg = input("You: ")

        if user_msg.strip().lower() in ("exit", "quit", "bye"):
            print("Bot: 👋 Okay, see you next time!")
            break

        # Ask Gemini (movie_brain handles memory)
        reply = ask_gemini(user_msg)
        print("\nBot:", reply)
        print("\n----------------------------------------\n")


if __name__ == "__main__":
    run()
