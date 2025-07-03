import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Optional: fallback if you want
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in environment or .env file")