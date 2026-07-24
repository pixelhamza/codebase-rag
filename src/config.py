import os

from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-3.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")