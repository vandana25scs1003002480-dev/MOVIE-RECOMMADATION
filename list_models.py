import google.generativeai as genai

API_KEY = "enter ur api key"  # your real key

genai.configure(api_key=API_KEY)

for m in genai.list_models():
    print(m.name, "→", m.supported_generation_methods)
