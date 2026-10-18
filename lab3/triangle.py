"""Класс вычислений (из лабораторной работы №1): определение типа треугольника."""
import math


class TriangleCalculator:
    def get_triangle_type(self, a, b, c):
        """Возвращает кортеж (тип_треугольника, сообщение_об_ошибке)."""
        try:
            a, b, c = float(a), float(b), float(c)
        except (TypeError, ValueError):
            return "", "Стороны должны быть числами"
        if not all(math.isfinite(x) for x in (a, b, c)):
            return "", "Стороны должны быть конечными числами"
        if min(a, b, c) <= 0:
            return "", "Стороны должны быть положительными"
        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", ""
        if a == b == c:
            return "равносторонний", ""
        if a == b or b == c or a == c:
            return "равнобедренный", ""
        return "разносторонний", ""
