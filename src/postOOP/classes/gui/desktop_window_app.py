import sys
from src.postOOP.classes.gui.qt_design import Ui_MainWindow
from PyQt6 import QtWidgets
from src.postOOP.classes.others.postprocess_executor import main
from src.postOOP.post_lister import PostLister


class DesktopWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.post_name_selected = self.comboBoxPostSelect.currentText()
        print(self.post_name_selected)
        self.post_obj_selected = PostLister.post_dict[self.post_name_selected]
        print(self.post_obj_selected)

        self.current_work_dir = self.lineEditPathToCWD.text()
        print(self.current_work_dir)
        self.comboBoxPostSelect.currentTextChanged.connect(self.post_selected)
        self.lineEditPathToCWD.textChanged.connect(self.path_changed)
        self.pushButton_PostprocessStart.clicked.connect(self.start_postprocess)
        self.pushButton_Path_CWD_update.clicked.connect(self.open_file_explorer)

    def open_file_explorer(self):
        pass

    def post_selected(self):
        print(f"post selected: {self.post_name_selected}")
        self.textEdit_LogOutput.append(f"post changed to {self.post_name_selected}")
        self.post_name_selected = self.comboBoxPostSelect.currentText()
        self.post_obj_selected = PostLister.post_dict[self.post_name_selected]

    def start_postprocess(self):
        self.textEdit_LogOutput.append(f"postprocessing started")
        main(post_obj=self.post_obj_selected, work_dir_path=self.current_work_dir)
        self.textEdit_LogOutput.append(f"postprocessing finished")

    def path_changed(self):
        self.current_work_dir = self.lineEditPathToCWD.text()
        print(f"Path changed to: {self.current_work_dir}")


def main_ui():
    app = QtWidgets.QApplication(sys.argv)
    window = DesktopWindowApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main_ui()
