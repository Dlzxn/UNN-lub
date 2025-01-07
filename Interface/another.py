from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QCursor, QIcon
import sys
import os
import json

from parser.unn_request import UnnRequest

def resource_path(relative_path):
    """Получить путь к ресурсу, работает как в упакованном, так и в обычном режиме"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(base_path, relative_path))

    print(f"Текущая рабочая директория: {os.getcwd()}")

    return os.path.join(base_path, relative_path)

class Another:
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


    def check_login(self):
        username = self.login_input.text()
        self.set_loading_cursor()

        self.log = UnnRequest(username)

        if self.log.proverka_user:  # Проверка реализуется в validate_login
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

    def logout_user(self):
        self.delete_user_data()
        self.registration_screen()
        self.main_layout.setCurrentWidget(self.main_layout.widget(self.main_layout.count() - 1))


    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("dddd, dd MMMM yyyy HH:mm:ss")
        self.time_label.setText(current_time)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_theme()
        self.update_theme()

    def update_theme(self):
        if hasattr(self, 'main_layout') and self.main_layout.currentWidget() is not None:
            print(f'[INFO] THEME-UPDATE')
            if self.dark_mode:
                self.main_layout.currentWidget().setStyleSheet("background-color: #2b2b2b; color: white;")
            else:
                self.main_layout.currentWidget().setStyleSheet("background-color: #0261c7; color: #315e0e;")

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


    def get_theme_style(self):
        if self.dark_mode:
            print(f'[INFO] THEME-"background-color: #3a3a3a; color: white;"')
            return "background-color: #3a3a3a; color: white;"
        else:
            return "background-color: white; color: black;"


