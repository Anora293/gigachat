import os
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()

client = GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"),
    scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
    model=os.getenv("GIGACHAT_MODEL", "GigaChat"),
    verify_ssl_certs=False,
)

def ask_gigachat(messages: list[dict]) -> str:
    response = client.chat({
        "model": os.getenv("GIGACHAT_MODEL", "GigaChat"),
        "messages": messages,
    })
    return response.choices[0].message.content
