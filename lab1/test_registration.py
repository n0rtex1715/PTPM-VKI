import unittest

# Импортируем функции из модуля registration для тестирования
from registration import (
    validate_registration,
    mask_password
)


class TestRegistration(unittest.TestCase):

    # 1. Успешная регистрация
    def test_valid_registration(self):
        result, message = validate_registration(
            "Peter_123",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertTrue(result)
        self.assertEqual(message, "")

    # 2. Пустой логин
    def test_empty_login(self):
        result, message = validate_registration(
            "",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)
        self.assertEqual(
            message,
            "Логин не может быть пустым"
        )

    # 3. Слишком короткий логин
    def test_short_login(self):
        result, message = validate_registration(
            "abc",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)

    # 4. Кириллица в обычном логине
    def test_cyrillic_login(self):
        result, message = validate_registration(
            "Петя123",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)

    # 5. Запрещённый логин
    def test_blacklisted_login(self):
        result, message = validate_registration(
            "admin",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)
        self.assertEqual(
            message,
            "Логин находится в черном списке"
        )

    # 6. Корректный телефон
    def test_valid_phone(self):
        result, message = validate_registration(
            "+7-999-123-4567",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertTrue(result)

    # 7. Некорректный телефон
    def test_invalid_phone(self):
        result, message = validate_registration(
            "+79991234567",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)

    # 8. Корректный email
    def test_valid_email(self):
        result, message = validate_registration(
            "test@example.com",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertTrue(result)

    # 9. Некорректный email
    def test_invalid_email(self):
        result, message = validate_registration(
            "test@example",
            "Секрет1!",
            "Секрет1!"
        )

        self.assertFalse(result)

    # 10. Слишком короткий пароль
    def test_short_password(self):
        result, message = validate_registration(
            "Peter_123",
            "Сек1!",
            "Сек1!"
        )

        self.assertFalse(result)

    # 11. Пароль с латиницей
    def test_latin_password(self):
        result, message = validate_registration(
            "Peter_123",
            "Password1!",
            "Password1!"
        )

        self.assertFalse(result)

    # 12. Нет заглавной буквы
    def test_password_without_uppercase(self):
        result, message = validate_registration(
            "Peter_123",
            "секрет1!",
            "секрет1!"
        )

        self.assertFalse(result)

    # 13. Нет строчной буквы
    def test_password_without_lowercase(self):
        result, message = validate_registration(
            "Peter_123",
            "СЕКРЕТ1!",
            "СЕКРЕТ1!"
        )

        self.assertFalse(result)

    # 14. Нет цифры
    def test_password_without_digit(self):
        result, message = validate_registration(
            "Peter_123",
            "Секрет!!",
            "Секрет!!"
        )

        self.assertFalse(result)

    # 15. Нет спецсимвола
    def test_password_without_special_character(self):
        result, message = validate_registration(
            "Peter_123",
            "Секрет12",
            "Секрет12"
        )

        self.assertFalse(result)

    # 16. Пароли не совпадают
    def test_password_confirmation_mismatch(self):
        result, message = validate_registration(
            "Peter_123",
            "Секрет1!",
            "Секрет2!"
        )

        self.assertFalse(result)
        self.assertEqual(
            message,
            "Пароль и подтверждение пароля не совпадают"
        )

    # 17. Проверка маскирования
    def test_password_masking_same_password(self):
        mask1 = mask_password("Секрет1!")
        mask2 = mask_password("Секрет1!")

        self.assertEqual(mask1, mask2)

    # 18. Разные пароли дают разные маски
    def test_password_masking_different_passwords(self):
        mask1 = mask_password("Секрет1!")
        mask2 = mask_password("Секрет2!")

        self.assertNotEqual(mask1, mask2)


if __name__ == "__main__":
    unittest.main()