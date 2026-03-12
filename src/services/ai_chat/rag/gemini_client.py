import google.generativeai as genai
from src.core.config import settings
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(question: str, context: str):

    prompt = f"""
    You are an agriculture expert assistant.

    Use the context to answer the farmer's question.

    Context:
    {context}

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text