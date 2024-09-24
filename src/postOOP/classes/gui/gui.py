from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt6.QtCore import QSize, Qt
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyPost")
        self.setFixedSize(QSize(int(1920 / 2), int(1080 / 2)))

        button1 = QPushButton("press me")
        button1.setCheckable(True)
        button1.clicked.connect(self.say_on_click)
        button1.clicked.connect(self.button_was_toggled)
        self.setCentralWidget(button1)

    def say_on_click(self):
        print("Clicked!")

    def button_was_toggled(self, checked):
        print(f"Checked? {checked}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
