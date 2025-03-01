from openai import OpenAI
from typing import Optional
from enum import Enum
from ai.constants import OPENROUTER_API_URL
from utils.providers.format import format_ai_response

class AiInterface(Enum):
    OPENROUTER = "openrouter"

class AIModels(Enum):
    DEEPSEEKR1 = "deepseek/deepseek-r1:free"
    DEEPSEEKR1_70 = "deepseek/deepseek-r1-distill-llama-70b:free"

class AIClient:
    """
    Base class for AI providers.
    """
    def ask(self, question: str) -> str:
        """
        Send a question to the AI provider and return the response.
        """
        raise NotImplementedError("Subclasses must implement the 'ask' method.")


class OpenRouterClient(AIClient):
    """
    Client for interacting with OpenRouter, which provides a unified interface for multiple LLMs.
    """
    def __init__(self, model: str = AIModels.DEEPSEEKR1_70.value, api_key: Optional[str] = None):
        """
        Initialize the OpenRouter client.

        Args:
            model (str): The model to use (e.g., "deepseek/deepseek-r1:free").
            api_key (str, optional): The OpenRouter API key. If not provided, it will be loaded from the environment.
        """
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(
            base_url=OPENROUTER_API_URL,
            api_key=self.api_key,
        )

    def ask(self, question: str, **kwargs) -> str:
        """
        Send a question to the OpenRouter API and return the response.

        Args:
            question (str): The question to ask.
            **kwargs: Additional arguments for the API request (e.g., headers, body).

        Returns:
            str: The AI's response.
        """

        # Make the API request
        completion = self.client.chat.completions.create(
            model=self.model,
            messages = [
                {
                    "role": "system",
                    "content": """
                    You are a concise and expert coding assistant.

                    **Your output must follow these rules strictly:**
                    1. If there is **one correct answer**, return it like this:
                    {
                        "data": ["answer"]
                    }
                    2. If there are **multiple correct answers**, return them as:
                    {
                        "data": ["answer1", "answer2", "answer3"]
                    }
                    3. **No extra explanation or commentary**—only return the required answer in the specified format.
                    4. If no language is mentioned, provide answers for the **5 most common languages**:
                    Python, JavaScript, Java, C++, and TypeScript.

                    **Examples:**

                    - Input: "How do I reverse an array in Python?"
                    Output:
                        {
                            "data": ["arr.reverse()"]
                        }

                    - Input: "How do I reverse an array?"
                    Output:
                    {
                        "data": [
                            "Python: arr.reverse()",
                            "JavaScript: arr.reverse()",
                            "Java: Collections.reverse(list);",
                            "C++: std::reverse(arr.begin(), arr.end());",
                            "TypeScript: arr.reverse()"
                        ]
                    }
                    """,
                },
                {
            "role": "user",
            "content": f"{question}",
        },]
            ,
        )
        return format_ai_response(completion.choices[0].message.content)


def get_ai_client(provider: str = "openrouter", **kwargs) -> AIClient:
    """
    Factory function to get an AI client for the specified provider.

    Args:
        provider (str): The AI provider to use (currently only "openrouter" is supported).
        **kwargs: Additional arguments to pass to the client constructor.

    Returns:
        AIClient: An instance of the specified AI client.
    """
    if provider == AiInterface.OPENROUTER.value:
        return OpenRouterClient(**kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider}")