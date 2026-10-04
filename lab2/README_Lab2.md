# Лабораторная работа №2 — Юнит-тестирование

## Среда разработки
Visual Studio Code + Python 3.x + встроенный `unittest`.

## Структура
- `src/registration.py` — метод из лабораторной работы №1.
- `src/delivery_service.py` — модуль расчета доставки с исправленными дефектами.
- `src/Delivery_original.py` — исходный предоставленный вариант для сравнения.
- `tests/test_registration.py` — 20 тестов для проекта из ЛР1.
- `tests/test_delivery.py` — 20 тестов для доставки.
- `Отчет_ЛР2_ФИО.docx` — отчет.

## Запуск
В терминале VS Code:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
python -m unittest discover -v
```

`unittest` входит в стандартную библиотеку Python, поэтому отдельная установка пакета не требуется.
