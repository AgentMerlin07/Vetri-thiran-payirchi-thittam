import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "LegalEase")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
# The PDF selected gemini-1.5-pro. Keep that value here if your API account
# still exposes it; otherwise set GEMINI_MODEL to a currently available model.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro").strip()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "6000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.35"))
