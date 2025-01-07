from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QFrame, QMessageBox, QStackedLayout, QScrollArea, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QPixmap, QCursor, QIcon
import sys
import os
import json

from Interface.another import resource_path


class Dev:
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
