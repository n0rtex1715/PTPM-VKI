from controller import Controller
from database import Database
from interfaces import ConsoleUserInterface, EmailService
from triangle import TriangleCalculator

if __name__ == "__main__":
    controller = Controller(TriangleCalculator(), Database("triangles.db"),
                            ConsoleUserInterface(), EmailService())
    print(controller.run())
