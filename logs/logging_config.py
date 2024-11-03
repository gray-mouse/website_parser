import logging

def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename="logs.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

app_logger = setup_logger()