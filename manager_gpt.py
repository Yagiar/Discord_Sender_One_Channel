import g4f
import g4f.debug
import httpx
from g4f.client import Client
from g4f.Provider import FreeChatgpt, Liaobots, Phind, RetryProvider
from openai import OpenAI
import openai

import config

g4f.debug.logging = False


class GptClient:
    def __init__(self, role: str, proxy: str = None) -> None:
        custom_http_client = httpx.Client(proxies=f"http://{config.GPT_PROXY}")
        self.client = OpenAI(
                api_key=config.OPENAI_API_KEY,
                http_client=custom_http_client,)
        self.role = role

    def get_message(self,):
        response = self.client.chat.completions.create(
            model=config.GPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": config.PROMPT,
                },
            ],
            temperature=config.TEMPERATURE,
            )
        return response.choices[0].message.content
