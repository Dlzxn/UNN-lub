from PyQt6.QtWidgets import (QMainWindow,
                             QWidget, QStackedLayout)
from PyQt6.QtGui import QIcon
import os


from Interface.another import Another, resource_path
from Interface.registration import Registration
from Interface.mainscreen import MainWindow
from Interface.schedule import Schedule
from Interface.dev import Dev


class UniversityApp(QMainWindow, Another, Registration, MainWindow, Schedule, Dev):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личный кабинет студента ННГУ")
        self.setFixedSize(1200, 800)

        self.setWindowIcon(QIcon(resource_path("Interface/icon/unn.png")))

        # Путь к теме и кешу
        self.theme_path = resource_path("theme.json")
        self.cache_path = resource_path("user.json")
        self.dark_mode = self.load_theme()
        self.update_theme()

        print(f"Текущая рабочая директория: {os.getcwd()}")

        self.main_layout = QStackedLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.user_data = self.load_user_data()
        self.init_ui()





