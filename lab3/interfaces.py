"""Абстрактные интерфейсы и их реализации: пользовательский ввод и сторонняя зависимость."""
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_input(self):
        """Возвращает кортеж из трёх значений (длины сторон)."""


class ConsoleUserInterface(UserInterface):
    def get_input(self):
        a = input("Введите длину стороны 1: ")
        b = input("Введите длину стороны 2: ")
        c = input("Введите длину стороны 3: ")
        return a, b, c


class ExternalService(ABC):
    @abstractmethod
    def send(self, message):
        """Передаёт строку стороннему процессу."""


class EmailService(ExternalService):
    """Имитация отправки данных на email-сервер."""

    def send(self, message):
        print(f"[EMAIL] Отправлено: {message}")
        return True
