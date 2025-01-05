from PyQt6.QtWidgets import QApplication

from Interface.menu import UniversityApp

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniversityApp()
    window.show()
    sys.exit(app.exec())


"""
[PYI-4175:ERROR] Failed to load Python shared library '/home/alex/dev/python/UNN-lub/myapp/usr/bin/_internal/libpython3.12.so.1.0': 
dlopen: /home/alex/dev/python/UNN-lub/myapp/usr/bin/_internal/libpython3.12.so.1.0: cannot open shared object file: No such file or directory

"""