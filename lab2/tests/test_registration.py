import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from registration import validate_registration, mask_password


class TestRegistration(unittest.TestCase):

    def test_accepts_valid_registration(self):
        result = validate_registration("Peter_123", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (True, ""))

    def test_rejects_empty_login(self):
        result = validate_registration("", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (False, "Логин не может быть пустым"))

    def test_rejects_short_login(self):
        result = validate_registration("abc", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    def test_rejects_login_with_cyrillic(self):
        result = validate_registration("Петя123", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    def test_rejects_login_with_forbidden_symbol(self):
        result = validate_registration("Peter-123", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    def test_rejects_blacklisted_login(self):
        result = validate_registration("admin", "Секрет1!", "Секрет1!")
        self.assertEqual(result, (False, "Логин находится в черном списке"))

    def test_accepts_phone_login(self):
        result = validate_registration("+7-999-123-4567", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    def test_rejects_invalid_phone_login(self):
        result = validate_registration("+79991234567", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    def test_accepts_email_login(self):
        result = validate_registration("test@example.com", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    def test_rejects_invalid_email_login(self):
        result = validate_registration("test@example", "Секрет1!", "Секрет1!")
        self.assertFalse(result[0])

    def test_accepts_minimum_length_username(self):
        result = validate_registration("abc12", "Секрет1!", "Секрет1!")
        self.assertTrue(result[0])

    def test_rejects_short_password(self):
        result = validate_registration("Peter_123", "Сек1!", "Сек1!")
        self.assertFalse(result[0])

    def test_rejects_latin_password(self):
        result = validate_registration("Peter_123", "Password1!", "Password1!")
        self.assertFalse(result[0])

    def test_rejects_password_without_uppercase(self):
        result = validate_registration("Peter_123", "секрет1!", "секрет1!")
        self.assertFalse(result[0])

    def test_rejects_password_without_lowercase(self):
        result = validate_registration("Peter_123", "СЕКРЕТ1!", "СЕКРЕТ1!")
        self.assertFalse(result[0])

    def test_rejects_password_without_digit(self):
        result = validate_registration("Peter_123", "Секрет!!", "Секрет!!")
        self.assertFalse(result[0])

    def test_rejects_password_without_special_character(self):
        result = validate_registration("Peter_123", "Секрет12", "Секрет12")
        self.assertFalse(result[0])

    def test_rejects_mismatched_password_confirmation(self):
        result = validate_registration("Peter_123", "Секрет1!", "Секрет2!")
        self.assertEqual(
            result,
            (False, "Пароль и подтверждение пароля не совпадают")
        )

    def test_masks_same_password_deterministically(self):
        self.assertEqual(mask_password("Секрет1!"), mask_password("Секрет1!"))

    def test_masks_different_passwords_differently(self):
        self.assertNotEqual(mask_password("Секрет1!"), mask_password("Секрет2!"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
