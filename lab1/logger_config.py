# Импортируем необходимые модули
import logging
import os
import sys


def setup_logger():
    # Создаем директорию для логов, если она не существует
    os.makedirs("logs", exist_ok=True)

    # Форматирование логов: время | уровень | сообщение + формат даты
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Настройка корневого логгера
    logging.basicConfig(
        # Минимальный уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        level=logging.DEBUG,
        # Форматирование логов и даты
        format=log_format,
        datefmt=date_format,
        # Обработчики логов: вывод в консоль и запись в файл
        handlers=[
            # Вывод в консоль
            logging.StreamHandler(sys.stdout),
            # Запись в файл с кодировкой UTF-8
            logging.FileHandler(
                "logs/file_txt.log",
                encoding="utf-8"
            )
        ],
        # Перезаписываем конфигурацию логгера, если она уже была настроена
        force=True
    )
    # Логируем успешную настройку логгера
    logging.info("Логгер успешно сконфигурирован")