# chatbot_v6.py
import logging
import requests

from api_client import GigaChatClient


def setup_logger():
    logger = logging.getLogger("ai_lab")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def make_request(url: str):
    """Делает GET-запрос и проверяет статус."""
    logger.info(f"Делаем запрос к {url}")

    try:
        response = requests.get(url, timeout=10)

        if 400 <= response.status_code < 500:
            logger.error(f"Клиентская ошибка: {response.status_code}")
            raise ValueError(f"Сервер сказал, что мы не правы. Код: {response.status_code}")

        if response.status_code >= 500:
            logger.error(f"Ошибка сервера: {response.status_code}")
            raise RuntimeError(f"Сервер прилёг. Код: {response.status_code}")

        logger.info("Запрос прошёл успешно!")
        return response

    except requests.exceptions.Timeout:
        logger.error("Запрос превысил 10 секунд.", exc_info=True)
        raise

    except requests.exceptions.ConnectionError:
        logger.error("Нет соединения с сервером.", exc_info=True)
        raise


def main():
    logger.info("Программа запущена")

    # 1. Тест с 4xx
    try:
        make_request("https://httpbin.org/status/400")
    except ValueError as e:
        logger.warning(f"Пользовательская ошибка: {e}")
    except RuntimeError as e:
        logger.error(f"Ошибка сервера: {e}")

    # 2. Тест с 5xx
    try:
        make_request("https://httpbin.org/status/500")
    except ValueError as e:
        logger.warning(f"Пользовательская ошибка: {e}")
    except RuntimeError as e:
        logger.error(f"Ошибка сервера: {e}")

    # 3. Реальный GigaChat с фейковым ключом
    client = GigaChatClient(api_key="ВАШ_FAKE_КЛЮЧ_ДЛЯ_ТЕСТА")

    try:
        answer = client.send_message("Напиши хайку про нейросети")
        print("Ответ GigaChat:", answer)

    except ValueError as e:
        logger.warning(f"Проблема с запросом: {e}")
        print(f"❌ {e}")

    except RuntimeError as e:
        logger.error(f"Проблема с сервером: {e}")
        print(f"💥 {e}")

    logger.info("Программа завершена")


if __name__ == "__main__":
    main()
