from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QCursor, QIcon
import sys
import os
import json

from Interface.another import resource_path


class Registration:
    def registration_screen(self):
        registration_widget = QWidget()
        registration_layout = QVBoxLayout()
        registration_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем всегда светлую тему для экрана регистрации
        registration_widget.setStyleSheet("background-color: #2072c9; color: white;")

        # Логотип и заголовок
        logo_label = QLabel()
        pixmap = QPixmap(resource_path("Interface/icon/unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        registration_layout.addWidget(logo_label)

        title_label = QLabel("Университет Лобачевского")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #fafcfc;")
        registration_layout.addWidget(title_label)
        print(f"Текущая рабочая директория: {os.getcwd()}")

        #clouds png
        background_label = QLabel(registration_widget)
        background_pixmap = QPixmap(resource_path("icon/clouds.png"))
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 1272, 284)
        background_label.lower()  # Отправляет виджет на задний план

        # Поле для логина
        login_input = QLineEdit()
        login_input.setPlaceholderText("Введите логин")
        login_input.setFixedWidth(300)
        login_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px; color: #edeff0;")
        self.login_input = login_input
        registration_layout.addWidget(login_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Войти"
        login_button = QPushButton("Войти")
        login_button.setStyleSheet(
            "padding: 10px; background-color: #0056b3; color: white; border: none; border-radius: 5px;")
        self.key = False
        login_button.clicked.connect(self.check_login)
        registration_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        registration_widget.setLayout(registration_layout)
        self.main_layout.addWidget(registration_widget)
