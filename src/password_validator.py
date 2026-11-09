def validate_password(password: str) -> bool:
    """
    Выполняет валидацию строки пароля на соответствие политикам безопасности.

    :param password: Проверяемый пароль
    :return: True, если пароль удовлетворяет всем условиям, иначе False
    :raises TypeError: Если входной параметр не является строкой
    :raises ValueError: Если входная строка содержит символы пробела
    """
    # Этап 1: Проверка входных данных и генерация исключений
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if ' ' in password:
        raise ValueError("Пароль не должен содержать пробелы")

    # Этап 2: Проверка критериев валидности пароля
    # 1. Длина строки: от 8 до 20 символов включительно
    if not (8 <= len(password) <= 20):
        return False

    # 2. Заглавные буквы: содержит как минимум одну заглавную букву
    has_upper = any(c.isupper() for c in password)
    if not has_upper:
        return False

    # 3. Строчные буквы: содержит как минимум одну строчную букву
    has_lower = any(c.islower() for c in password)
    if not has_lower:
        return False

    # 4. Цифры: содержит как минимум одну десятичную цифру
    has_digit = any(c.isdigit() for c in password)
    if not has_digit:
        return False

    # 5. Специальные символы: содержит как минимум один символ из набора !@#$%^&*
    special_chars = {'!', '@', '#', '$', '%', '^', '&', '*'}
    has_special = any(c in special_chars for c in password)
    if not has_special:
        return False

    return True
