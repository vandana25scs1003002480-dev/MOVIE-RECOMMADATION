print("START OF FILE")

import google.generativeai as genai

print("IMPORT DONE")

API_KEY = "enter api key"
print("API KEY LOADED")

genai.configure(api_key=API_KEY)
print("CONFIG DONE")

model = genai.GenerativeModel("gemini-2.5-pro")

print("MODEL LOADED")

resp = model.generate_content("hello")
print("RESPONSE:", resp.text)
