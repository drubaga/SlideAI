from src.prompts.prompt_templates import PRESENTATION_TEMPLATE

class PromptManager:
    @staticmethod
    def get_system_prompt(context: str) -> str:
        return PRESENTATION_TEMPLATE.format(context=context)
