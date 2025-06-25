"""
PromptManager class for building prompts using raw templates and user input.
"""

from src.prompts.prompt_templates import PRESENTATION_TEMPLATE

class PromptManager:

    @staticmethod
    def build_presentation_prompt(context: str, user_query: str) -> str:
        """
        Formats the presentation template with user query and source context.

        Args:
            context (str): The content of the uploaded file.
            user_query (str): The user instruction for the assistant.

        Returns:
            str: A formatted prompt ready for LLM input.
        """
        return f"""{PRESENTATION_TEMPLATE}

### User Query:
{user_query}

---

### Source Text:
{context}

---

Make sure the output is valid JSON, well-structured, and follows the requested slide structure.
"""
