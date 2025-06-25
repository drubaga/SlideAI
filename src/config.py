import os
from dotenv import load_dotenv

"""
Configuration module for loading environment variables and model parameters.
"""

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings (safe defaults)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o") 
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.1))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 1500))
