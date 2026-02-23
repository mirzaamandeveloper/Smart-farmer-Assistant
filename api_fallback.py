
import google.generativeai as genai
import os

# 🔑 Set your Gemini API key as environment variable: GEMINI_API_KEY
# Or replace below with your API key (not recommended for production)
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_response(question):
    prompt = f"You are an agriculture expert helping farmers.\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text