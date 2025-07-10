# config.py

import os
from dotenv import load_dotenv

"""
Configuration module for loading environment variables and model parameters.
"""

# Load variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_model = "gpt-4o"
openai_temperature = 0.1
openai_max_tokens = 1500


# API Keys for Image Providers
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
