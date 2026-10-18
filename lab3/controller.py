"""Класс-контроллер со сквозной бизнес-логикой."""


class Controller:
    def __init__(self, calculator, database, user_interface, external_service):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def run(self):
        a, b, c = self.user_interface.get_input()

        record = self.database.get_record(a, b, c)
        if record is None:
            triangle_type, error = self.calculator.get_triangle_type(a, b, c)
            self.database.add_record(a, b, c, triangle_type, error)
        else:
            triangle_type, error = record["triangle_type"], record["error_message"]

        result = f"Ошибка: {error}" if error else f"Тип треугольника: {triangle_type}"
        self.external_service.send(result)
        return result
