import os
import requests
import logging
from dotenv import load_dotenv

from exceptions import UserInputError, ServerSideError, RateLimitError

load_dotenv()

logger = logging.getLogger("ai_lab")


class GigaChatClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def send_message(self, prompt):
        payload = {
            "model": os.getenv("GIGACHAT_MODEL", "GigaChat"),
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            # Таймаут 15 секунд — чтобы не висеть вечно
            response = requests.post(
                self.url, json=payload, headers=self.headers, timeout=15
            )

            # 1. Обработка HTTP-кодов
            if response.status_code == 401:
                raise UserInputError("API-ключ недействителен или не указан.")

            if response.status_code == 429:
                raise RateLimitError(retry_after=60)

            if response.status_code >= 500:
                raise ServerSideError("Внутренняя ошибка серверов GigaChat.")

            # Если пришёл другой 4xx — тоже считаем ошибкой пользователя
            if 400 <= response.status_code < 500:
                raise UserInputError(f"Ошибка запроса: {response.status_code}")

            # 2. Если статус 200, но JSON пустой или без choices
            data = response.json()
            if not data.get("choices"):
                raise ServerSideError(f"API вернул пустой ответ: {data.get('detail')}")

            return data["choices"][0]["message"]["content"]

        # 3. Сетевые ошибки (таймаут, нет соединения)
        except requests.exceptions.Timeout:
            logger.warning("Запрос к GigaChat превысил 15 секунд.")
            raise ServerSideError("Таймаут соединения с нейросетью.")

        except requests.exceptions.ConnectionError:
            logger.warning("Нет соединения с сервером GigaChat.")
            raise ServerSideError("Проверьте интернет-соединение.")

        # 4. Ловим ошибки, которые выбросили сами выше
        except ApiLabError as e:
            logger.error(f"Бизнес-ошибка GigaChat: {e}")
            raise