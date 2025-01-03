from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap
import sys
import os
import json

class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личный кабинет студента ННГУ")
        self.setFixedSize(1200, 800)

        # Путь к теме и кешу
        self.theme_path = os.path.join(os.path.dirname(__file__), "theme.json")
        self.cache_path = os.path.join(os.path.dirname(__file__), "cache", "user.json")
        self.dark_mode = self.load_theme()

        self.main_layout = QStackedLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.user_data = self.load_user_data()
        self.init_ui()

    def load_theme(self):
        try:
            if os.path.exists(self.theme_path):
                with open(self.theme_path, 'r') as f:
                    data = json.load(f)
                    return data.get('theme', False)
            else:
                return False
        except Exception:
            return False

    def save_theme(self):
        try:
            with open(self.theme_path, 'w') as f:
                json.dump({'theme': self.dark_mode}, f)
        except Exception as e:
            self.show_error("Ошибка", f"Не удалось сохранить тему: {str(e)}")

    def load_user_data(self):
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, 'r') as f:
                    return json.load(f)
            else:
                return None
        except Exception:
            return None

    def save_user_data(self, username):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump({'username': username}, f)

    def init_ui(self):
        if self.user_data:
            self.main_screen()
        else:
            self.registration_screen()

    def registration_screen(self):
        registration_widget = QWidget()
        registration_layout = QVBoxLayout()
        registration_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Логотип и заголовок
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        registration_layout.addWidget(logo_label)

        title_label = QLabel("Университет Лобачевского")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        registration_layout.addWidget(title_label)

        # Поле для логина
        login_input = QLineEdit()
        login_input.setPlaceholderText("Введите логин")
        login_input.setFixedWidth(300)
        login_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        self.login_input = login_input
        registration_layout.addWidget(login_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка "Войти"
        login_button = QPushButton("Войти")
        login_button.setStyleSheet(
            "padding: 10px; background-color: #0056b3; color: white; border: none; border-radius: 5px;")
        login_button.clicked.connect(self.check_login)
        registration_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        registration_widget.setLayout(registration_layout)
        self.main_layout.addWidget(registration_widget)

    def check_login(self):
        username = self.login_input.text()
        if username:  # Проверка должна быть реализована вашей функцией
            self.save_user_data(username)
            self.main_screen()
        else:
            self.show_error("Ошибка", "Введите корректный логин.")

    def main_screen(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхняя панель
        header_layout = QHBoxLayout()

        # Логотип
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setFixedSize(50, 50)
        header_layout.addWidget(logo_label)

        # Время
        time_label = QLabel()
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.time_label = time_label
        self.update_time()

        # Таймер для обновления времени
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        header_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка переключения темы
        theme_button = QPushButton("Тема")
        theme_button.setStyleSheet("padding: 5px; margin: 5px;")
        theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(theme_button, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(header_layout)

        # Расписание
        schedule_frame = QFrame()
        schedule_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 10px;")
        schedule_layout = QVBoxLayout()
        schedule_frame.setLayout(schedule_layout)

        self.day_buttons = []
        for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
            day_button = QPushButton(day)
            day_button.setStyleSheet(
                "padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; background-color: #f0f8ff;")
            day_button.clicked.connect(lambda checked, d=day: self.show_day_schedule(d))
            self.day_buttons.append(day_button)
            schedule_layout.addWidget(day_button)

        main_layout.addWidget(schedule_frame)
        main_widget.setLayout(main_layout)
        self.main_layout.addWidget(main_widget)
        self.main_layout.setCurrentWidget(main_widget)

    def show_day_schedule(self, day):
        self.clear_schedule()
        for btn in self.day_buttons:
            btn.setStyleSheet(
                "padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 5px; background-color: #f0f8ff;")

        selected_button = next(btn for btn in self.day_buttons if btn.text() == day)
        selected_button.setStyleSheet(
            "padding: 10px; margin: 5px; border: 1px solid #0056b3; border-radius: 5px; background-color: #cfe2ff;")

        details_layout = QVBoxLayout()
        fields = ["Предмет: Математика", "Время: 10:00 - 11:30", "Аудитория: 101", "Преподаватель: Иванов И.И."]
        for field in fields:
            field_label = QLabel(field)
            field_label.setStyleSheet("font-size: 16px; margin: 5px; padding: 5px;")
            details_layout.addWidget(field_label)

        selected_button.setLayout(details_layout)

    def clear_schedule(self):
        for btn in self.day_buttons:
            btn.setLayout(None)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dddd, dd MMMM yyyy HH:mm:ss")
        self.time_label.setText(current_time)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_theme()
        self.update_theme()

    def update_theme(self):
        style = "background-color: #2e2e2e; color: white;" if self.dark_mode else "background-color: white; color: black;"
        self.setStyleSheet(style)

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec())
