import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from delivery_service import calculate_delivery_cost


class TestDelivery(unittest.TestCase):

    # Ожидаемые даты рассчитаны от фиксированной даты отправки в сервисе:
    # 2026-09-03.
    def test_calculates_basic_delivery_cost(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "обычный"),
            (700, "2026-09-04")
        )

    # Граничные значения веса 0.1 и 50 кг допустимы, значения за ними —
    # нет. При неверных параметрах сервис возвращает (-1, "0000-00-00").
    def test_accepts_minimum_weight(self):
        self.assertEqual(
            calculate_delivery_cost(0.1, 100, "обычный"),
            (700, "2026-09-04")
        )

    def test_accepts_maximum_weight(self):
        self.assertEqual(
            calculate_delivery_cost(50, 100, "обычный"),
            (1050, "2026-09-04")
        )

    def test_rejects_weight_below_minimum(self):
        self.assertEqual(
            calculate_delivery_cost(0.09, 100, "обычный"),
            (-1, "0000-00-00")
        )

    def test_rejects_weight_above_maximum(self):
        self.assertEqual(
            calculate_delivery_cost(50.01, 100, "обычный"),
            (-1, "0000-00-00")
        )

    def test_accepts_minimum_distance(self):
        self.assertEqual(
            calculate_delivery_cost(1, 1, "обычный"),
            (205, "2026-09-04")
        )

    def test_accepts_500_kilometers(self):
        self.assertEqual(
            calculate_delivery_cost(1, 500, "обычный"),
            (2700, "2026-09-04")
        )

    def test_assigns_two_days_for_501_kilometers(self):
        self.assertEqual(
            calculate_delivery_cost(1, 501, "обычный"),
            (2705, "2026-09-05")
        )

    def test_accepts_maximum_distance(self):
        self.assertEqual(
            calculate_delivery_cost(1, 5000, "обычный"),
            (25200, "2026-09-13")
        )

    def test_rejects_zero_distance(self):
        self.assertEqual(
            calculate_delivery_cost(1, 0, "обычный"),
            (-1, "0000-00-00")
        )

    def test_rejects_distance_above_maximum(self):
        self.assertEqual(
            calculate_delivery_cost(1, 5001, "обычный"),
            (-1, "0000-00-00")
        )

    def test_rejects_unknown_package_type(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "нестандартный"),
            (-1, "0000-00-00")
        )

    # Доплаты за тип посылки и коэффициенты веса проверяются отдельно,
    # чтобы ошибки в одном тарифном правиле не маскировали другое.
    def test_adds_fragile_package_fee(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "хрупкий"),
            (1000, "2026-09-04")
        )

    def test_adds_dangerous_package_fee(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "опасный"),
            (1700, "2026-09-04")
        )

    def test_applies_medium_weight_coefficient(self):
        self.assertEqual(
            calculate_delivery_cost(10, 100, "обычный"),
            (840, "2026-09-04")
        )

    def test_applies_heavy_weight_coefficient(self):
        self.assertEqual(
            calculate_delivery_cost(20, 100, "обычный"),
            (1050, "2026-09-04")
        )

    def test_does_not_apply_coefficient_at_five_kilograms(self):
        self.assertEqual(
            calculate_delivery_cost(5, 100, "обычный"),
            (700, "2026-09-04")
        )

    # Экспресс меняет цену и срок доставки; на границе срока округление
    # вверх важно, например, для расстояния 1500 км.
    def test_halves_cost_for_express_delivery(self):
        self.assertEqual(
            calculate_delivery_cost(1, 100, "обычный", True),
            (350, "2026-09-04")
        )

    def test_express_delivery_for_1000_km_takes_one_day(self):
        self.assertEqual(
            calculate_delivery_cost(1, 1000, "обычный", True),
            (2600, "2026-09-04")
        )

    def test_express_delivery_for_1500_km_rounds_up_to_two_days(self):
        self.assertEqual(
            calculate_delivery_cost(1, 1500, "обычный", True),
            (3850, "2026-09-05")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
