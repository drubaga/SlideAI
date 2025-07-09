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

# Image Generation Configuration
# IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "pexels").lower()  # Options: "pexels", "serpapi"
# ENABLE_IMAGES = os.getenv("ENABLE_IMAGES", "true").lower() == "true"

# API Keys for Image Providers
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ENABLE_IMAGES = True
# IMAGE_PROVIDER =  "serpapi"
#"pexels"  