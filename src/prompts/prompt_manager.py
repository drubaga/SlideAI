# 📁 src/prompts/prompt_manager.py
from src.prompts.prompt_templates import PRESENTATION_TEMPLATE

class PromptManager:
    @staticmethod
    def get_system_prompt(context: str) -> str:
        """
        Returns the instruction-style system prompt (without user input).
        """
        return f"""{PRESENTATION_TEMPLATE}

--- 

### Source Text:
{context}

--- 

Make sure the output is valid JSON, well-structured, and follows the requested slide structure.
"""