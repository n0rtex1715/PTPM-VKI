import logging

from logger_config import setup_logger
from registration import validate_registration


def main():
    setup_logger()

    logging.info("Приложение запущено")

    # Ожидаем ввод пользователя
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    confirmation = input("Подтвердите пароль: ")

    # Вызываем функцию проверки регистрации и получаем результат
    result, message = validate_registration(
        login,
        password,
        confirmation
    )

    print("\nРезультат:", result)

    if message:
        print("Ошибка:", message)

    # Логируем результат регистрации
    logging.info(
        "Результат регистрации: result=%s, message=%s",
        result,
        message
    )


if __name__ == "__main__":
    main()