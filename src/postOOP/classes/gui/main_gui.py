import sys
from src.postOOP.classes.gui.qt_design import Ui_MainWindow
from PyQt6 import QtWidgets


class ExapmleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExapmleApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
