from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QCursor, QIcon
import sys
import os
import json

from Interface.another import resource_path


class MainWindow:
    def main_screen(self):
        self.set_loading_cursor()
        try:
            with open(resource_path("Interface/user.json"), 'r') as file:
                data = json.load(file)
                self.u = UnnRequest(data['username'])
        except Exception as er:
            print(f"[ERROR] Enternet Connection Error: {er}")
        self.unset_loading_cursor()

        main_widget = QWidget()
        background_label = QLabel(main_widget)
        main_layout = QVBoxLayout()

        # Верхняя панель
        header_layout = QHBoxLayout()

        # Логотип
        logo_label = QLabel()
        pixmap = QPixmap(resource_path("Interface/icon/unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setFixedSize(50, 50)
        header_layout.addWidget(logo_label)

        # Время
        time_label = QLabel()
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #f5f5f5;")
        self.time_label = time_label
        self.update_time()

        # Таймер для обновления времени
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        header_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка переключения темы
        theme_button = QPushButton("Тема")
        theme_button.setStyleSheet("padding: 5px; margin: 5px; color: white; border: true;")
        theme_button.clicked.connect(self.toggle_theme)


        header_layout.addWidget(theme_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка DEV
        dev_button = QPushButton("DEV")
        dev_button.setStyleSheet("padding: 5px; margin: 5px; background-color: #ffa500; color: white; border: none;")
        dev_button.clicked.connect(self.show_dev_info)
        header_layout.addWidget(dev_button, alignment=Qt.AlignmentFlag.AlignRight)


        main_layout.addLayout(header_layout)

        # clouds png
        background_label = QLabel(main_widget)
        background_pixmap = QPixmap(resource_path("Interface/icon/clouds.png"))
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 1272, 284)
        background_label.lower()  # Отправляет виджет на задний план



        # Блок расписания
        schedule_frame = QScrollArea()
        schedule_frame.setWidgetResizable(True)
        schedule_content = QWidget()
        schedule_layout = QVBoxLayout()
        schedule_layout.setSpacing(5)  # Уменьшенное расстояние между элементами
        schedule_content.setLayout(schedule_layout)
        schedule_frame.setWidget(schedule_content)

        # clouds png
        background_label = QLabel(schedule_content)
        background_pixmap = QPixmap(resource_path("Interface/icon/clouds.png"))
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 636, 142)
        background_label.lower()  # Отправляет виджет на задний план

        for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
            day_button = QPushButton(day)
            day_button.setStyleSheet(
                "padding: 10px; margin: 5px; border-radius: 10px; background-color: #f0f8ff; color: #0056b3; border: 1px solid #ccc;")
            day_button.clicked.connect(lambda checked, d=day: self.show_day_schedule(d))

            schedule_layout.addWidget(day_button)

        # Кнопка выхода из профиля
        logout_button = QPushButton("Выход")
        logout_button.setStyleSheet("padding: 5px; margin: 5px; background-color: #d9534f; color: white; border: none;")
        logout_button.clicked.connect(self.logout_user)
        header_layout.addWidget(logout_button, alignment=Qt.AlignmentFlag.AlignRight)


        main_layout.addWidget(schedule_frame)
        main_widget.setLayout(main_layout)
        self.main_layout.addWidget(main_widget)
        self.main_layout.setCurrentWidget(main_widget)
        self.update_theme()