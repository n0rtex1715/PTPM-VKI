import unittest
from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):
    """Тестовый класс для функции validate_password"""

    # 1. Позитивное тестирование
    def test_valid_password_latin(self):
        """Проверка корректного пароля на латинице"""
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_password_cyrillic(self):
        """Проверка корректного пароля на кириллице"""
        self.assertTrue(validate_password("ПарольТест9#"))

    # 2. Анализ граничных значений длины (BVA)
    def test_boundary_length_7(self):
        """Длина 7 символов (на 1 меньше границы)"""
        self.assertFalse(validate_password("Pass1!a"))

    def test_boundary_length_8(self):
        """Длина 8 символов (нижняя граница)"""
        self.assertTrue(validate_password("Pass1!ab"))

    def test_boundary_length_20(self):
        """Длина 20 символов (верхняя граница)"""
        self.assertTrue(validate_password("SecurePassword123!@#"))

    def test_boundary_length_21(self):
        """Длина 21 символ (на 1 больше границы)"""
        password = "A" * 17 + "a1!b"  # 17 + 4 = 21
        self.assertFalse(validate_password(password))

    # 3. Классы эквивалентности (неполный состав символов)
    def test_missing_uppercase(self):
        """Пароль без заглавных букв"""
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        """Пароль без строчных букв"""
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        """Пароль без цифр"""
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special_char(self):
        """Пароль без специальных символов"""
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char_underscore(self):
        """Пароль со спецсимволом, не входящим в перечень (символ _)"""
        self.assertFalse(validate_password("SecurePass1_"))

    def test_invalid_special_char_question(self):
        """Пароль со спецсимволом, не входящим в перечень (символ ?)"""
        self.assertFalse(validate_password("SecurePass1?"))

    # 4. Тестирование исключительных ситуаций
    def test_space_in_middle(self):
        """Проверка выброса ValueError при наличии пробела внутри строки"""
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_space_at_start(self):
        """Проверка выброса ValueError при наличии пробела в начале строки"""
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_space_at_end(self):
        """Проверка выброса ValueError при наличии пробела в конце строки"""
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_type_error_none(self):
        """Проверка выброса TypeError при передаче None"""
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_type_error_int(self):
        """Проверка выброса TypeError при передаче int"""
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_type_error_list(self):
        """Проверка выброса TypeError при передаче list"""
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s", "1", "!"])

    def test_empty_string(self):
        """Пустая строка нарушает правила длины и состава"""
        self.assertFalse(validate_password(""))


if __name__ == '__main__':
    unittest.main()
