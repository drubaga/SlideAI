import os
from dotenv import load_dotenv

"""
Configuration module for loading environment variables and model parameters.
"""

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_model = "gpt-4o"
openai_temperature  = 0.1 
openai_max_tokens = 1500
