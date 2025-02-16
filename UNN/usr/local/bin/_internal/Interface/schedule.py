from PyQt6.QtWidgets import (QLabel, QPushButton,
                             QVBoxLayout, QWidget, QFrame, QScrollArea)
from PyQt6.QtCore import Qt


from Interface.another import resource_path
from analytic.analyhtml import AnalyticHtml

class Schedule:
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

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        days: str = ""
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
        scroll_area.setFixedHeight(700)

        # Кнопка возврата
        back_button = QPushButton("Назад")
        back_button.setStyleSheet("padding: 10px; background-color: #0056b3; color: white; border-radius: 5px;")
        back_button.clicked.connect(self.main_screen)
        day_schedule_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        day_schedule_widget.setLayout(day_schedule_layout)
        self.main_layout.addWidget(day_schedule_widget)
        self.main_layout.setCurrentWidget(day_schedule_widget)


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