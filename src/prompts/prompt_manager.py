from src.prompts.prompt_templates import PRESENTATION_TEMPLATE

# context bellow is the data folder 
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

Return only the JSON object. Do not use markdown formatting or escape characters. Do not wrap it in triple backticks. Use single braces only.

"""