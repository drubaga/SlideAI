from src.prompts.prompt_templates import PRESENTATION_TEMPLATE

class PromptManager:
    """Manages prompt formatting for system instructions."""
    @staticmethod
    def get_system_prompt(context: str) -> str:
        """
        Formats and returns the system prompt with the given context.

        Args:
            context (str): The input context to include in the system prompt.

        Returns:
            str: A formatted system prompt string.
        """
        return PRESENTATION_TEMPLATE.format(context=context)
