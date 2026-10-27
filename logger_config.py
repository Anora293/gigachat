import logging


def setup_logger():
    logger = logging.getLogger("ai_lab")
    logger.setLevel(logging.DEBUG)

    # Чтобы не дублировать хендлеры при повторном вызове
    if logger.handlers:
        return logger

    # Хендлер в консоль (только INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Хендлер в файл (всё подряд, включая DEBUG)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Формат: время | уровень | файл:строка | сообщение
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger