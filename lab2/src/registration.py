import re
import hashlib

BLACKLIST = {
    "admin",
    "administrator",
    "root",
    "user",
    "test",
    "support",
}


def mask_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_hash[:12]


def validate_login(login: str) -> tuple[bool, str]:
    if not login:
        return False, "Логин не может быть пустым"

    phone_pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    username_pattern = r"^[A-Za-z0-9_]+$"

    if re.fullmatch(phone_pattern, login):
        return True, ""

    if re.fullmatch(email_pattern, login):
        return True, ""

    if len(login) < 5:
        return False, "Логин должен содержать минимум 5 символов"

    if not re.fullmatch(username_pattern, login):
        return False, (
            "Логин может содержать только латинские буквы, "
            "цифры и знак подчеркивания"
        )

    if login.lower() in BLACKLIST:
        return False, "Логин находится в черном списке"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    allowed_pattern = r"^[А-Яа-яЁё0-9\W_]+$"

    if not re.fullmatch(allowed_pattern, password, re.UNICODE):
        return False, (
            "Пароль может содержать только кириллицу, "
            "цифры и специальные символы"
        )

    if not re.search(r"[А-ЯЁ]", password):
        return False, "Пароль должен содержать хотя бы одну букву в верхнем регистре"

    if not re.search(r"[а-яё]", password):
        return False, "Пароль должен содержать хотя бы одну букву в нижнем регистре"

    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"

    if not re.search(r"[^\w\s]", password, re.UNICODE):
        return False, "Пароль должен содержать хотя бы один специальный символ"

    return True, ""


def validate_registration(
    login: str,
    password: str,
    password_confirmation: str
) -> tuple[bool, str]:
    valid, message = validate_login(login)
    if not valid:
        return False, message

    valid, message = validate_password(password)
    if not valid:
        return False, message

    if password != password_confirmation:
        return False, "Пароль и подтверждение пароля не совпадают"

    return True, ""
