from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from datetime import datetime, timedelta
import sys
import os
import json


from Interface.another import resource_path, Another
from parser.unn_request import UnnRequest



class MainWindow:
    def main_screen(self):
        self.set_loading_cursor()

        try:
            with open(resource_path("analytic/cache/user.json"), 'r') as file:
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
        theme_button = QPushButton()
        theme_button.setIcon(QIcon(resource_path("Interface/icon/moon_icon.png")))
        theme_button.setIconSize(QSize(25, 25))
        theme_button.setStyleSheet("padding: 5px; margin: 5px; color: white; border: true;")
        theme_button.clicked.connect(self.toggle_theme)


        # Кнопка DEV
        dev_button = QPushButton()
        dev_button.setIcon(QIcon(resource_path("Interface/icon/dev.png")))
        dev_button.setIconSize(QSize(30, 30))
        dev_button.setStyleSheet("padding: 5px; margin: 5px;color: white; border: none;")
        dev_button.clicked.connect(self.show_dev_info)

        # Кнопка выхода из профиля
        logout_button = QPushButton("Выход")
        logout_button.setStyleSheet("padding: 5px; margin: 5px; background-color: #d9534f; color: white; border: none;")


        logout_button.clicked.connect(self.logout_user)

        # Основная кнопка
        self.menu_button = QPushButton("Mеню", self)
        self.menu_button.clicked.connect(self.toggle_menu)

        # Полноэкранное меню
        self.menu = QWidget(self)
        self.menu.setStyleSheet("background-color: rgba(50, 50, 50, 230); border-radius: 10px;")
        self.menu.setGeometry(0, 300, 400, 300)  # Начальная позиция (вне экрана)

        # Лэйаут для меню
        menu_layout = QVBoxLayout(self.menu)
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Кнопки внутри меню
        for text in ["Главная", "Настройки", "О программе", "Закрыть"]:
            btn = QPushButton(text)
            btn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #777; color: white;")
            btn.clicked.connect(self.toggle_menu)  # Закрывать меню при нажатии
            menu_layout.addWidget(btn)

        btn = QPushButton("Dev")
        btn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #777; color: white;")
        btn.clicked.connect(self.show_dev_info)  # Закрывать меню при нажатии
        menu_layout.addWidget(btn)

        btn = QPushButton("Главная")
        btn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #777; color: white;")
        btn.clicked.connect(self.show_dev_info)  # Закрывать меню при нажатии
        menu_layout.addWidget(btn)

        # Основной лэйаут
        layout = QVBoxLayout(self)
        layout.addWidget(self.menu_button)
        layout.addWidget(QLabel("Основное окно"))  # Просто для примера

        self.setLayout(layout)

        # Создаём анимацию
        self.animation = QPropertyAnimation(self.menu, b"geometry")
        self.animation.setDuration(500)  # Длительность анимации (мс)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)  # Плавный эффект

        self.menu_visible = False  # Флаг состояния меню


        # self.browser = QWebEngineView()
        # with open("Interface/Web-interface/main_menu.html", "r") as file:
        #     self.browser.setHtml(file.read())

        """container with buttons """
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(10)
        icon_layout.addWidget(dev_button)
        icon_layout.addWidget(theme_button)
        icon_layout.addWidget(logout_button)
        icon_layout.addWidget(self.browser)

        header_layout.addLayout(icon_layout)
        header_layout.setAlignment(icon_layout, Qt.AlignmentFlag.AlignRight)


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


        for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
            day_button = QPushButton(day)
            day_button.setStyleSheet(
                "padding: 10px; margin: 5px; border-radius: 10px; background-color: #f0f8ff; color: #0056b3; border: 1px solid #ccc;")
            day_button.clicked.connect(lambda checked, d=day: self.show_day_schedule(d))

            schedule_layout.addWidget(day_button)

        self.current_date = datetime.now()  # Устанавливаем текущую дату как начальную

        # Блок с выбором недели
        week_navigation_layout = QHBoxLayout()
        week_navigation_layout.setSpacing(5)  # Небольшое расстояние между элементами
        week_navigation_layout.setContentsMargins(0, 0, 0, 0)  # Убираем внешние отступы

        # Кнопка на прошлую неделю (стрелка влево)
        prev_week_button = QPushButton("←")
        prev_week_button.setFixedSize(30, 30)  # Фиксированный размер кнопки
        prev_week_button.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        prev_week_button.clicked.connect(self.show_previous_week)

        # Актуальная дата
        current_week_label = QLabel()
        current_week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_week_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.current_week_label = current_week_label  # Сохраняем для обновлений
        self.update_current_week_label()

        # Кнопка на следующую неделю (стрелка вправо)
        next_week_button = QPushButton("→")
        next_week_button.setFixedSize(30, 30)  # Фиксированный размер кнопки
        next_week_button.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        next_week_button.clicked.connect(self.show_next_week)

        # Добавляем кнопки и дату в макет
        week_navigation_layout.addWidget(prev_week_button)
        week_navigation_layout.addWidget(current_week_label)
        week_navigation_layout.addWidget(next_week_button)
        week_navigation_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Все элементы слева

        # Добавляем макет выбора недели над расписанием
        main_layout.addLayout(week_navigation_layout)

        # clouds png
        background_label = QLabel(schedule_content)
        background_pixmap = QPixmap(resource_path("Interface/icon/clouds.png"))
        background_label.setPixmap(background_pixmap)
        background_label.setScaledContents(True)
        background_label.setGeometry(0, 0, 636, 142)
        background_label.lower()  # Отправляет виджет на задний план


        main_layout.addWidget(schedule_frame)
        main_widget.setLayout(main_layout)
        main_layout.addLayout(layout)

        self.main_layout.addWidget(main_widget)
        self.main_layout.setCurrentWidget(main_widget)
        self.update_theme()


    def toggle_menu(self):
        """Анимированное открытие/закрытие меню"""
        if self.menu_visible:
            self.animation.setStartValue(self.menu.geometry())
            self.animation.setEndValue(self.menu.geometry().adjusted(0, -300, 0, -300))  # Убираем вверх
        else:
            self.animation.setStartValue(self.menu.geometry().adjusted(0, -300, 0, -300))  # Начинаем сверху
            self.animation.setEndValue(self.menu.geometry())  # Опускаем вниз

        self.animation.start()
        self.menu_visible = not self.menu_visible  # Меняем состояние меню

    def show_update_message(self):
        # Показываем стильное окно с уведомлением о новой версии
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Обновление доступно!")
        msg.setText("<b>Доступна новая версия приложения!</b>")
        msg.setInformativeText(
            "Мы рекомендуем скачать последнюю версию, чтобы воспользоваться всеми "
            "новыми функциями и улучшениями.<br>"
            "<a href='https://github.com/Dlzxn/UNN-lub/releases'>Скачать новую версию</a>"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.button(QMessageBox.StandardButton.Ok).setText("Понял!")
        msg.setTextFormat(Qt.TextFormat.RichText)  # Включение HTML-форматирования текста
        msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)  # Для кликабельных ссылок

        # Устанавливаем изображение слева
        pixmap = QPixmap(resource_path("Interface/icon/unn.png"))  # Укажите путь к изображению
        msg.setIconPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))

        msg.exec()

    def create_page(self, text):
        """Создаёт страницу с текстом"""
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(text)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def switch_page(self, index):
        """Меняет страницу в QStackedWidget"""
        self.pages.setCurrentIndex(index)


    def update_current_week_label(self):
        """Обновляет отображение текущей недели."""
        self.current_week_label.setText(self.current_date.strftime("Неделя: %d.%m.%Y"))

    def show_previous_week(self):
        """Переключает на прошлую неделю."""

        self.current_date -= timedelta(weeks=1)
        self.update_current_week_label()
        self.u.init__previous()
        # Здесь добавь обновление расписания для новой даты, если требуется

    def show_next_week(self):
        """Переключает на следующую неделю."""
        self.current_date += timedelta(weeks=1)
        self.update_current_week_label()
        self.u.init__next()
        # Здесь добавь обновление расписания для новой даты, если требуется

