import hashlib
import re

# Список запрещённых имён пользователей.
# Такие значения блокируются при регистрации, чтобы исключить типовые
# служебные логины вроде "admin" или "root".
BLACKLIST = {
    "admin",
    "administrator",
    "root",
    "user",
    "test",
    "support",
}


def mask_password(password: str) -> str:
    # Преобразуем пароль в байты, затем вычисляем SHA-256.
    # Это позволяет сравнивать пароли без сохранения исходного значения
    # в открытом виде, что важно для безопасного хранения.
    password_bytes = password.encode("utf-8")
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_hash[:12]


def validate_login(login: str) -> tuple[bool, str]:
    # Проверяем пустой логин в самом начале: без него дальнейшая проверка
    # не имеет смысла, поэтому возвращаем понятную ошибку пользователю.
    if not login:
        return False, "Логин не может быть пустым"

    # Для логина разрешены три формата:
    # 1. номер телефона в формате +7-999-123-4567;
    # 2. электронная почта;
    # 3. обычное имя пользователя латиницей, цифрами и нижним подчёркиванием.
    phone_pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    username_pattern = r"^[A-Za-z0-9_]+$"

    if re.fullmatch(phone_pattern, login):
        return True, ""

    if re.fullmatch(email_pattern, login):
        return True, ""

    # Если логин не телефон и не email, он должен соответствовать формату
    # обычного имени пользователя. Для него есть минимальная длина.
    if len(login) < 5:
        return False, "Логин должен содержать минимум 5 символов"

    if not re.fullmatch(username_pattern, login):
        return False, (
            "Логин может содержать только латинские буквы, "
            "цифры и знак подчеркивания"
        )

    # После проверки формата проверяем, не является ли логин служебным.
    if login.lower() in BLACKLIST:
        return False, "Логин находится в черном списке"

    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    # Минимальная длина пароля задаёт базовый уровень сложности.
    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов"

    # В пароле разрешены кириллица, цифры и любые символы, не относящиеся
    # к пробелам и буквам/цифрам. Это даёт свободу для создания сложного
    # шифра, но в то же время запрещает недопустимые символы.
    allowed_pattern = r"^[А-Яа-яЁё0-9\W_]+$"

    if not re.fullmatch(allowed_pattern, password, re.UNICODE):
        return False, (
            "Пароль может содержать только кириллицу, "
            "цифры и специальные символы"
        )

    # Каждая проверка ниже подтверждает один из критериев надёжного пароля:
    # 1) хотя бы одна буква верхнего регистра;
    # 2) хотя бы одна буква нижнего регистра;
    # 3) хотя бы одна цифра;
    # 4) хотя бы один специальный символ.
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
    # Сначала проверяем логин, потому что если он некорректен, нет смысла
    # переходить к дальнейшей валидации уже введённых данных.
    valid, message = validate_login(login)
    if not valid:
        return False, message

    # Затем проверяем надёжность пароля.
    valid, message = validate_password(password)
    if not valid:
        return False, message

    # Последней проверкой является сверка подтверждения пароля с исходным.
    if password != password_confirmation:
        return False, "Пароль и подтверждение пароля не совпадают"

    return True, ""
