from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap
import sys
import json
import os

class UniversityScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расписание Университета")
        self.setFixedSize(1000, 800)

        # Путь к теме и иконкам
        self.theme_path = os.path.join(os.path.dirname(__file__), "theme.json")
        self.icon_path = os.path.join(os.path.dirname(__file__), "icon")

        # Загружаем тему
        self.dark_mode = self.load_theme()

        # Центральный виджет и основной layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Загружаем данные пользователя
        self.user_logged_in = False  # Симуляция проверки логина
        self.initUI()

    def load_theme(self):
        try:
            if os.path.exists(self.theme_path):
                with open(self.theme_path, 'r') as f:
                    data = json.load(f)
                    return data.get('theme', False)
            else:
                self.show_error("Ошибка", "Файл с темой не найден.")
                return False
        except Exception as e:
            self.show_error("Ошибка при загрузке темы", f"Произошла ошибка при загрузке темы: {str(e)}")
            return False

    def save_theme(self):
        try:
            with open(self.theme_path, 'w') as f:
                json.dump({'theme': self.dark_mode}, f)
        except Exception as e:
            self.show_error("Ошибка при сохранении темы", f"Не удалось сохранить тему: {str(e)}")

    def initUI(self):
        if self.user_logged_in:
            self.show_main_menu()
        else:
            self.show_registration_screen()

    def show_registration_screen(self):
        # Очищаем layout
        self.clear_layout(self.layout)

        # Layout регистрации
        registration_layout = QVBoxLayout()
        registration_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Логотип
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(self.icon_path, "unn_logo_blue_U.png"))
        if pixmap.isNull():
            self.show_error("Ошибка загрузки изображения", "Не удалось загрузить логотип.")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        registration_layout.addWidget(logo_label)

        # Название университета
        university_label = QLabel("Университет Лобачевского")
        university_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        university_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        registration_layout.addWidget(university_label)

        # Поле ввода логина
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setFixedWidth(300)
        self.login_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")
        registration_layout.addWidget(self.login_input)

        # Кнопка "Войти"
        submit_button = QPushButton("Войти")
        submit_button.setStyleSheet("padding: 10px; background-color: #0056b3; color: white; border: none; border-radius: 5px;")
        submit_button.clicked.connect(self.check_login)
        registration_layout.addWidget(submit_button)

        self.layout.addLayout(registration_layout)

    def show_main_menu(self):
        # Очищаем layout
        self.clear_layout(self.layout)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Шапка с логотипом и временем
        header_layout = QHBoxLayout()

        # Логотип справа
        logo_label = QLabel()
        pixmap = QPixmap(os.path.join(self.icon_path, "unn_logo_blue_U.png"))
        if pixmap.isNull():
            self.show_error("Ошибка загрузки изображения", "Не удалось загрузить логотип.")
        logo_label.setPixmap(pixmap)
        logo_label.setFixedSize(50, 50)
        header_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(header_layout)

        # Панель времени
        time_bar = QLabel()
        time_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        time_bar.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        self.time_bar = time_bar
        self.update_time()
        main_layout.addWidget(time_bar)

        # Таймер для обновления времени каждую секунду
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        # Основное содержимое
        schedule_frame = QFrame()
        schedule_frame.setStyleSheet(self.get_schedule_frame_style())
        schedule_frame.setFixedSize(900, 600)

        schedule_layout = QVBoxLayout()
        schedule_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        schedule_frame.setLayout(schedule_layout)

        # Кнопки для дней недели
        for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
            day_button = QPushButton(day)
            day_button.setStyleSheet(self.get_day_button_style())
            day_button.setFixedSize(800, 60)
            day_button.clicked.connect(lambda checked, d=day: self.show_day_details(d, schedule_layout))
            schedule_layout.addWidget(day_button)

        main_layout.addWidget(schedule_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(main_layout)

    def show_day_details(self, day, layout):
        # Очищаем layout перед показом деталей
        self.clear_layout(layout)

        # Отображаем расписание для выбранного дня
        day_label = QLabel(f"Расписание на {day}")
        day_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(day_label)

        # Поля для расписания
        fields = ["Название:", "Время:", "Преподаватель:", "Аудитория:"]
        for field in fields:
            field_label = QLabel(field)
            field_label.setStyleSheet(self.get_field_label_style())
            layout.addWidget(field_label)

        # Кнопка "Назад"
        back_button = QPushButton("Назад к расписанию")
        back_button.setStyleSheet("padding: 10px; background-color: #0056b3; color: white; border: none; border-radius: 5px;")
        back_button.clicked.connect(self.show_main_menu)
        layout.addWidget(back_button)

    def check_login(self):
        # Симуляция проверки логина
        if self.login_input.text():
            self.user_logged_in = True
            self.show_main_menu()
        else:
            self.show_error("Ошибка логина", "Пожалуйста, введите логин.")

    def update_time(self):
        current_datetime = QDateTime.currentDateTime().toString("dddd, dd MMMM yyyy HH:mm:ss")
        self.time_bar.setText(current_datetime)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_theme()
        self.setStyleSheet(self.get_app_style())
        self.show_main_menu()

    def get_app_style(self):
        if self.dark_mode:
            return "background-color: #2e2e2e; color: white;"
        return "background-color: white; color: black;"

    def get_schedule_frame_style(self):
        if self.dark_mode:
            return "background-color: #444; border-radius: 15px;"
        return "background-color: white; border-radius: 15px;"

    def get_day_button_style(self):
        if self.dark_mode:
            return "padding: 10px; border: 1px solid #666; border-radius: 5px; background-color: #555; color: white;"
        return "padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f0f8ff;"

    def get_field_label_style(self):
        if self.dark_mode:
            return "margin: 5px; padding: 10px; border: 1px solid #666; border-radius: 5px; background-color: #333; color: white;"
        return "margin: 5px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;"

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_error(self, title, message):
        # Выводим ошибку на экран
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityScheduleApp()
    window.setStyleSheet(window.get_app_style())
    window.show()
    sys.exit(app.exec())
