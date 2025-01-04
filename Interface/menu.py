from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QCursor
import sys
import os
import json

from parser.unn_request import UnnRequest
from analytic.analyhtml import AnalyticHtml

class UniversityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Личный кабинет студента ННГУ")
        self.setFixedSize(1200, 800)

        # Путь к теме и кешу
        self.theme_path = os.path.join(os.path.dirname(__file__), "theme.json")
        self.cache_path = os.path.join(os.path.dirname(__file__), "user.json")
        self.dark_mode = self.load_theme()
        self.update_theme()

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

        # Устанавливаем всегда светлую тему для экрана регистрации
        registration_widget.setStyleSheet("background-color: #2072c9; color: white;")


        # Логотип и заголовок
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icon/unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        registration_layout.addWidget(logo_label)

        title_label = QLabel("Университет Лобачевского")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #fafcfc;")
        registration_layout.addWidget(title_label)

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

    def check_login(self):
        username = self.login_input.text()
        self.set_loading_cursor()

        self.log = UnnRequest(username, 0)

        if self.log.proverka_user():  # Проверка реализуется в validate_login
            self.save_user_data(username)
            self.main_screen()
            self.unset_loading_cursor()
        else:
            self.show_error("Ошибка", "Неверный логин. Попробуйте снова.")
            self.login_input.clear()  # Очищаем только поле логина, без пересоздания экрана
            self.unset_loading_cursor()

    def validate_login(self, username):
        # Симуляция проверки логина (замените на реальную логику проверки)
        allowed_users = ["user1", "user2", "student"]  # Пример списка разрешенных логинов
        return username in allowed_users

    def delete_user_data(self):
        try:
            if os.path.exists(self.cache_path):
                os.remove(self.cache_path)
        except Exception as e:
            self.show_error("Ошибка", f"Не удалось удалить данные пользователя: {str(e)}")

    def main_screen(self):
        self.set_loading_cursor()
        try:
            with open("Interface/user.json", 'r') as file:
                data = json.load(file)
                self.u = UnnRequest(data['username'])
        except Exception as er:
            print(f"[ERROR] Enternet Connection Error: {er}")
        self.unset_loading_cursor()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхняя панель
        header_layout = QHBoxLayout()

        # Логотип
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "icon/unn_logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
            logo_label.setFixedSize(50, 50)
        header_layout.addWidget(logo_label)

        # Время
        time_label = QLabel()
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0056b3;")
        self.time_label = time_label
        self.update_time()

        # Таймер для обновления времени
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        header_layout.addWidget(time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка переключения темы
        theme_button = QPushButton("Тема")
        theme_button.setStyleSheet("padding: 5px; margin: 5px; color: white; border: none;")
        theme_button.clicked.connect(self.toggle_theme)


        header_layout.addWidget(theme_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Кнопка DEV
        dev_button = QPushButton("DEV")
        dev_button.setStyleSheet("padding: 5px; margin: 5px; background-color: #ffa500; color: white; border: none;")
        dev_button.clicked.connect(self.show_dev_info)
        header_layout.addWidget(dev_button, alignment=Qt.AlignmentFlag.AlignRight)


        main_layout.addLayout(header_layout)

        # Блок расписания
        schedule_frame = QScrollArea()
        schedule_frame.setWidgetResizable(True)
        schedule_content = QWidget()
        schedule_layout = QVBoxLayout()
        schedule_layout.setSpacing(5)  # Уменьшенное расстояние между элементами
        schedule_content.setLayout(schedule_layout)
        schedule_frame.setWidget(schedule_content)

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

    def logout_user(self):
        self.delete_user_data()
        self.registration_screen()
        self.main_layout.setCurrentWidget(self.main_layout.widget(self.main_layout.count() - 1))

    def show_day_schedule(self, day):
        day_schedule_widget = QWidget()
        day_schedule_layout = QVBoxLayout()

        # Заголовок дня
        day_label = QLabel(f"Расписание на {day}")
        day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        day_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0056b3;")
        day_schedule_layout.addWidget(day_label)

        analys =  AnalyticHtml()
        schedule_data = analys.set_slovar()
        print("shedule:", schedule_data)
        # schedule_data = {
        #     "Пн": [
        #         {"День": "Понедельник", "Название": "Математика", "Преподаватель": "Иванов И.И.", "Аудитория": "101",
        #          "Время": "10:00 - 11:30"},
        #         {"День": "Понедельник", "Название": "Физика", "Преподаватель": "Петров П.П.", "Аудитория": "202",
        #          "Время": "12:00 - 13:30"}
        #     ],
        #     "Вт": [
        #         {"День": "Вторник", "Название": "Химия", "Преподаватель": "Сидоров С.С.", "Аудитория": "303",
        #          "Время": "14:00 - 15:30"}
        #     ]
            # Добавьте остальные дни недели
        # }

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        match day:
            case "Понедельник":
                days = "Пн"
            case "Вторник":
                days = "Вт"
            case "Среда":
                days = "Ср"
            case "Четверг":
                days = "Чт"
            case "Пятница":
                days = "Пт"
            case "Суббота":
                days = "Сб"
            case "Воскресенье":
                days  = "Вс"


        # Добавляем предметы для выбранного дня
        if days in schedule_data:
            self.add_schedule_items(scroll_layout, schedule_data[days])

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        day_schedule_layout.addWidget(scroll_area)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        day_schedule_layout.addWidget(scroll_area)
        scroll_area.setFixedHeight(800)

        # Кнопка возврата
        back_button = QPushButton("Назад")
        back_button.setStyleSheet("padding: 10px; background-color: #0056b3; color: white; border-radius: 5px;")
        back_button.clicked.connect(self.main_screen)
        day_schedule_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        day_schedule_widget.setLayout(day_schedule_layout)
        self.main_layout.addWidget(day_schedule_widget)
        self.main_layout.setCurrentWidget(day_schedule_widget)

    def get_theme_style(self):
        if self.dark_mode:
            return "background-color: #3a3a3a; color: white;"
        else:
            return "background-color: white; color: black;"

    def add_schedule_items(self, layout, subjects):
        for subject in subjects:
            print("subject:", subject)
            subject_widget = QFrame()
            subject_widget.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; margin: 5px; padding: 10px; background-color: #f0f8ff;")
            subject_layout = QVBoxLayout()

            for key, value in subject.items():
                print(f"{key}: {value}")
                label = QLabel(f"{key}: {value}")
                label.setStyleSheet("padding: 1px; color: #0056b3;")
                subject_layout.addWidget(label)

            subject_widget.setLayout(subject_layout)
            layout.addWidget(subject_widget)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dddd, dd MMMM yyyy HH:mm:ss")
        self.time_label.setText(current_time)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_theme()
        self.update_theme()

    def update_theme(self):
        if hasattr(self, 'main_layout') and self.main_layout.currentWidget() is not None:
            if self.dark_mode:
                self.main_layout.currentWidget().setStyleSheet("background-color: #434445; color: white;")
            else:
                self.main_layout.currentWidget().setStyleSheet("background-color: #006ce0; color: #b3b3b3;")

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def set_loading_cursor(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))

    def unset_loading_cursor(self):
        QApplication.restoreOverrideCursor()

    def show_dev_info(self):
        dev_widget = QWidget()
        dev_layout = QVBoxLayout()

        dev_label = QLabel("Dev: DlzxnDev (3824б1ма1)")
        dev_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffa500;")
        dev_layout.addWidget(dev_label)

        repo_label = QLabel("Repository: <a href='https://github.com/Dlzxn/UNN-lub'>https://github.com/Dlzxn/UNN-lub</a>")
        repo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        repo_label.setStyleSheet("font-size: 16px; color: #0056b3;")
        repo_label.setOpenExternalLinks(True)
        dev_layout.addWidget(repo_label)

        tg_label = QLabel("Tg: illgettomorow")
        tg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tg_label.setStyleSheet("font-size: 16px; color: #0056b3;")
        dev_layout.addWidget(tg_label)

        ver_label = QLabel("Version: 1.0")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver_label.setStyleSheet("font-size: 16px; color: #0056b3;")
        dev_layout.addWidget(ver_label)

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("padding: 10px; background-color: #0056b3; color: white; border-radius: 5px;")
        back_button.clicked.connect(self.main_screen)
        dev_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        dev_widget.setLayout(dev_layout)
        self.main_layout.addWidget(dev_widget)
        self.main_layout.setCurrentWidget(dev_widget)

