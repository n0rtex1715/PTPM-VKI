import sys
import unittest
from pathlib import Path

# Добавляем каталог src в путь поиска модулей, чтобы тесты могли импортировать
# функцию регистрации напрямую без установки пакета.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from registration import mask_password, validate_registration


# Набор тестов проверяет все основные сценарии регистрации: корректные случаи,
# ошибки в логине, ошибки в пароле, несовпадение подтверждения и безопасное
# маскирование пароля.
class TestRegistration(unittest.TestCase):

    # Успешная регистрация должна пройти, если логин и пароль соответствуют
    # требованиям и подтверждение совпадает с исходным паролем.
    def test_accepts_valid_registration(self):
        result = validate_registration("Peter_123", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (True, ""))

    # Пустой логин запрещён, потому что пользователь должен всегда иметь имя.
    def test_rejects_empty_login(self):
        result = validate_registration("", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (False, "Логин не может быть пустым"))

    # Логин должен быть длиннее минимального допустимого значения.
    def test_rejects_short_login(self):
        result = validate_registration("abc", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    # Для имени пользователя запрещена кириллица: допустимы только латиница,
    # цифры и символ подчёркивания.
    def test_rejects_login_with_cyrillic(self):
        result = validate_registration("Петя123", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    # Запрещённые символы вроде дефиса не допускаются в обычном логине.
    def test_rejects_login_with_forbidden_symbol(self):
        result = validate_registration("Peter-123", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    # Служебные логины из чёрного списка запрещены, чтобы исключить типовые
    # значения, которые могут создавать конфликты или быть опасными.
    def test_rejects_blacklisted_login(self):
        result = validate_registration("admin", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (False, "Логин находится в черном списке"))

    # Телефон может использоваться как логин, если подан в ожидаемом формате.
    def test_accepts_phone_login(self):
        result = validate_registration("+7-999-123-4567", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    # Номер без разделителей или в неверном формате не считается валидным.
    def test_rejects_invalid_phone_login(self):
        result = validate_registration("+79991234567", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    # Электронная почта корректного формата разрешена как логин.
    def test_accepts_email_login(self):
        result = validate_registration("test@example.com", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    # Невалидный email должен отвергаться до завершения регистрации.
    def test_rejects_invalid_email_login(self):
        result = validate_registration("test@example", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    # Минимально допустимая длина имени пользователя должна пройти проверку.
    def test_accepts_minimum_length_username(self):
        result = validate_registration("abc12", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    # Короткий пароль должен не проходить валидацию из-за низкой сложности.
    def test_rejects_short_password(self):
        result = validate_registration("Peter_123", "Сек1!", "Сек1!")
        self.assertFalse(result[0])

    # Пароль на латинице не подходит, потому что в проекте требуется кириллица.
    def test_rejects_latin_password(self):
        result = validate_registration("Peter_123", "Password1!", "Password1!")
        self.assertFalse(result[0])

    # Проверяем, что пароль обязательно содержит хотя бы одну заглавную букву.
    def test_rejects_password_without_uppercase(self):
        result = validate_registration("Peter_123", "секрет1!", "секрет1!")
        self.assertFalse(result[0])

    # Также требуется наличие хотя бы одной строчной буквы.
    def test_rejects_password_without_lowercase(self):
        result = validate_registration("Peter_123", "СЕКРЕТ1!", "СЕКРЕТ1!")
        self.assertFalse(result[0])

    # Цифра обязательна: пароль без цифр считается недостаточно надёжным.
    def test_rejects_password_without_digit(self):
        result = validate_registration("Peter_123", "Секрет!!", "Секрет!!")
        self.assertFalse(result[0])

    # Спецсимволы усиливают сложность пароля, поэтому без них проверка должна
    # завершаться ошибкой.
    def test_rejects_password_without_special_character(self):
        result = validate_registration("Peter_123", "Секрет12", "Секрет12")
        self.assertFalse(result[0])

    # Подтверждение пароля должно быть идентичным исходному значению.
    def test_rejects_mismatched_password_confirmation(self):
        result = validate_registration("Peter_123", "Секрет1!", "Секрет2!")
        self.assertEqual(
            result,
            (False, "Пароль и подтверждение пароля не совпадают")
        )

    # Функция маскировки должна быть детерминированной: один и тот же пароль
    # всегда даёт одинаковую маску.
    def test_masks_same_password_deterministically(self):
        self.assertEqual(mask_password("Секрет1!"), mask_password("Секрет1!"))

    # Для разных паролей должны получаться разные маски, чтобы избежать
    # коллизий при сравнении или отображении.
    def test_masks_different_passwords_differently(self):
        self.assertNotEqual(mask_password("Секрет1!"), mask_password("Секрет2!"))


if __name__ == "__main__":
    # Запуск тестов напрямую с подробным выводом для удобства отладки.
    unittest.main(verbosity=2)
