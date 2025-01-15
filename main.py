from PyQt6.QtWidgets import QApplication

from Interface.menu import UniversityApp

import sys

if __name__ == "__main__":
    """Start our program"""
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec())

