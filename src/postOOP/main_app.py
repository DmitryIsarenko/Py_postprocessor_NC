import sys
from PyQt6 import QtWidgets
from src.postOOP.classes.gui.desktop_window_app import DesktopWindowApp

import logging
logger = logging.getLogger("src")

#
# если запускаем в режиме из проекта, то в
# 58 линии
# файла
# src/postOOP/classes/gui/qt_design.py
# изменить 2 строки. 2 раскомментировать, 2 закоментировать
#


def main_ui():
    app = QtWidgets.QApplication(sys.argv)
    window = DesktopWindowApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    logger.info(f"Started execution from {__name__}")
    print(__name__)
    main_ui()
