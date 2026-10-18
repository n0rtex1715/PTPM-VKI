import unittest
from unittest.mock import Mock, patch

from controller import Controller
from database import Database
from interfaces import (ConsoleUserInterface, EmailService, ExternalService,
                        UserInterface)
from triangle import TriangleCalculator


def make_controller(inputs, calculator=None):
    """Controller с настоящими калькулятором и БД, но с заглушками ввода и сервера."""
    ui = Mock(spec=UserInterface)
    ui.get_input.return_value = inputs
    service = Mock(spec=ExternalService)
    db = Database(":memory:")
    calc = calculator or TriangleCalculator()
    return Controller(calc, db, ui, service), ui, service, db


class ControllerIntegrationTests(unittest.TestCase):
    # ---- интеграционные тесты ----
    def test_new_data_is_calculated_saved_and_sent(self):
        ctrl, ui, service, db = make_controller(("3", "3", "3"))
        result = ctrl.run()
        self.assertEqual(result, "Тип треугольника: равносторонний")
        self.assertEqual(db.get_record("3", "3", "3")["triangle_type"], "равносторонний")
        service.send.assert_called_once_with(result)

    def test_existing_record_is_taken_from_db_without_calculation(self):
        calc = Mock(wraps=TriangleCalculator())
        ctrl, ui, service, db = make_controller(("3", "4", "5"), calc)
        first = ctrl.run()
        second = ctrl.run()
        self.assertEqual(first, second)
        self.assertEqual(first, "Тип треугольника: разносторонний")
        calc.get_triangle_type.assert_called_once()  # второй раз — из БД
        self.assertEqual(service.send.call_count, 2)

    def test_invalid_input_error_is_stored_and_sent(self):
        ctrl, ui, service, db = make_controller(("abc", "1", "1"))
        result = ctrl.run()
        self.assertEqual(result, "Ошибка: Стороны должны быть числами")
        self.assertEqual(db.get_record("abc", "1", "1")["error_message"],
                         "Стороны должны быть числами")
        service.send.assert_called_once_with(result)
        # повторный запуск берёт ошибку из БД
        self.assertEqual(ctrl.run(), result)

    def test_console_ui_with_patched_input_and_email_stub(self):
        ctrl = Controller(TriangleCalculator(), Database(), ConsoleUserInterface(),
                          EmailService())
        with patch("builtins.input", side_effect=["2", "2", "3"]), \
                patch("builtins.print") as fake_print:
            result = ctrl.run()
        self.assertEqual(result, "Тип треугольника: равнобедренный")
        fake_print.assert_called_once_with(f"[EMAIL] Отправлено: {result}")

    # ---- изоляция контроллера полностью на заглушках ----
    def test_controller_isolated_with_all_mocks(self):
        ui = Mock(spec=UserInterface)
        ui.get_input.return_value = ("1", "2", "3")
        db = Mock(spec=Database)
        db.get_record.return_value = None
        calc = Mock(spec=TriangleCalculator)
        calc.get_triangle_type.return_value = ("не треугольник", "")
        service = Mock(spec=ExternalService)

        result = Controller(calc, db, ui, service).run()

        calc.get_triangle_type.assert_called_once_with("1", "2", "3")
        db.add_record.assert_called_once_with("1", "2", "3", "не треугольник", "")
        service.send.assert_called_once_with("Тип треугольника: не треугольник")
        self.assertEqual(result, "Тип треугольника: не треугольник")


class SupportingClassesTests(unittest.TestCase):
    def test_database_add_get_delete(self):
        db = Database()
        self.assertIsNone(db.get_record(1, 2, 3))
        db.add_record(1, 2, 3, "не треугольник")
        db.add_record(1, 2, 3, "не треугольник")  # повторная вставка заменяет запись
        self.assertEqual(db.get_record(1, 2, 3),
                         {"triangle_type": "не треугольник", "error_message": ""})
        self.assertTrue(db.delete_record(1, 2, 3))
        self.assertFalse(db.delete_record(1, 2, 3))
        self.assertIsNone(db.get_record(1, 2, 3))
        db.close()

    def test_calculator_edge_branches(self):
        calc = TriangleCalculator()
        self.assertEqual(calc.get_triangle_type("nan", 1, 1)[1],
                         "Стороны должны быть конечными числами")
        self.assertEqual(calc.get_triangle_type(0, 1, 1)[1],
                         "Стороны должны быть положительными")
        self.assertEqual(calc.get_triangle_type(None, 1, 1)[1],
                         "Стороны должны быть числами")
        self.assertEqual(calc.get_triangle_type(1, 2, 3), ("не треугольник", ""))

    def test_abstract_interfaces_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            UserInterface()
        with self.assertRaises(TypeError):
            ExternalService()


if __name__ == "__main__":
    unittest.main()
