import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Keys and Exchange Settings
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
BASE_URL = os.getenv("BASE_URL")
GPT_ROLE = "signal_generator"  # Options: "signal_generator", "strategy_explainer", "sentiment_analyzer"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")