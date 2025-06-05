import openai
import os

class GPTHandler:
    def __init__(self, api_key: str = None):
        """Inicializa el Handler de OpenAPI"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)

    def exec_response_api(self, instruction: str, input: str, bot_temp: float = 0.3) -> str:
        """Client con el esquema de instructions + input"""
        response = self.client.responses.create(
            model="gpt-4o",
            instructions=instruction,
            input=input,
            temperature=bot_temp
        )
        return response.output_text

    def exec_chat_api(self, messages: list, bot_temp: float = 0.3) -> str:
        """Client en formato de chat con lista de mensajes"""
        gpt_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=bot_temp
        )
        return gpt_response.choices[0].message.content.strip()
