# re для регулярных выражений, hashlib для хэширования паролей, logging для логирования
import re
import hashlib
import logging


# Предустановленный черный список логинов
BLACKLIST = {
    "admin",
    "administrator",
    "root",
    "user",
    "test",
    "support"
}


def mask_password(password: str) -> str:
    """
    Маскирование пароля для логов.
    Одинаковые пароли дают одинаковый результат,
    разные пароли — разные результаты.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()[:12]


def validate_login(login: str) -> tuple[bool, str]:
    """Проверяет логин."""

    if not login:
        return False, "Логин не может быть пустым"

    # Телефон: +x-xxx-xxx-xxxx
    phone_pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"

    # Email test@example.com
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    # Обычный логин (только латинские буквы, цифры и знак подчеркивания)
    username_pattern = r"^[A-Za-z0-9_]+$"

    # Проверяем, является ли логин телефоном или email
    if re.fullmatch(phone_pattern, login):
        return True, ""

    if re.fullmatch(email_pattern, login):
        return True, ""

    # Если нет, то проверяем обычный логин на длину символом
    if len(login) < 5:
        return False, "Логин должен содержать минимум 5 символов"

    # Проверяем обычный логин на соответствие шаблону
    if not re.fullmatch(username_pattern, login):
        return False, (
            "Логин может содержать только латинские буквы, "
            "цифры и знак подчеркивания"
        )

    # Проверяем, если находится в черном списке
    if login.lower() in BLACKLIST:
        return False, "Логин находится в черном списке"

    return True, ""

# Проверка пароля на соответствие требованиям безопасности
# Содержит минимум 7 символов, хотя бы одну букву в верхнем регистре,
# хотя бы одну букву в нижнем регистре, хотя бы одну цифру и хотя бы один спецсимвол
def validate_password(password: str) -> tuple[bool, str]:
    """Проверяет пароль."""

    # Проверяем длину пароля
    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    # По условию разрешены кириллица, цифры и спецсимволы.
    # Латинские буквы запрещены.
    allowed_pattern = r"^[А-Яа-яЁё0-9\W_]+$"

    if not re.fullmatch(allowed_pattern, password, re.UNICODE):
        return False, (
            "Пароль может содержать только кириллицу, "
            "цифры и специальные символы"
        )

    # Проверяем наличие хотя бы одной буквы в верхнем регистре,
    if not re.search(r"[А-ЯЁ]", password):
        return False, "Пароль должен содержать хотя бы одну букву в верхнем регистре"
    # в нижнем регистре,
    if not re.search(r"[а-яё]", password):
        return False, "Пароль должен содержать хотя бы одну букву в нижнем регистре"
    # хотя бы одну цифру,
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    # хотя бы один спецсимвол (не буква и не цифра)
    if not re.search(r"[^\w\s]", password, re.UNICODE):
        return False, "Пароль должен содержать хотя бы один специальный символ"

    return True, ""


def validate_registration(
    login: str,
    password: str,
    password_confirmation: str
) -> tuple[bool, str]:
    # Проверяет регистрацию пользователя, логирует процесс и возвращает результат проверки.

    masked_password = mask_password(password)
    masked_confirmation = mask_password(password_confirmation)

    # Логируем входные данные, маскируя пароли
    logging.info(
        "Проверка регистрации: login=%s, password=%s, confirmation=%s",
        login,
        masked_password,
        masked_confirmation
    )

    try:
        # Проверка логина
        valid, message = validate_login(login)

        if not valid:
            logging.warning(
                "Регистрация отклонена: login=%s, причина=%s",
                login,
                message
            )
            return False, message

        # Проверка пароля
        valid, message = validate_password(password)

        # Если пароль не прошел проверку, логируем причину и возвращаем результат
        if not valid:
            logging.warning(
                "Регистрация отклонена: login=%s, причина=%s",
                login,
                message
            )
            return False, message

        # Проверка совпадения паролей
        if password != password_confirmation:
            message = "Пароль и подтверждение пароля не совпадают"

            # Логируем причину отклонения регистрации
            logging.warning(
                "Регистрация отклонена: login=%s, причина=%s",
                login,
                message
            )

            return False, message

        # Логируем успешную проверку регистрации
        logging.info(
            "Регистрация успешно прошла проверку: login=%s, result=True",
            login
        )

        return True, ""

    # Если возникла непредвиденная ошибка, логируем её как критическую
    except Exception:
        logging.exception(
            "Критическая ошибка при проверке регистрации: login=%s",
            login
        )

        return False, "Внутренняя ошибка приложения"