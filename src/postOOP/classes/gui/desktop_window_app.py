import sys
import os
import logging
import time
from pprint import pprint
from time import sleep

from src.postOOP.classes.gui.qt_design import Ui_MainWindow
from PyQt6 import QtWidgets
# from src.postOOP.classes.others.postprocess_executor import execute_postprocess
from src.postOOP.post_lister import PostLister

from src.postOOP import config

logger = logging.getLogger(__name__)


class DesktopWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    config.POST_NAME = PostLister().default_post_name
    config.POST_OBJ = PostLister().default_post_obj

    def __init__(self):
        logger.info("Started init of window.")
        super().__init__()
        self.setupUi(self)

        if not config.STARTS_FROM_EXE:
            self.set_cwd_if_started_from_project()
        elif config.STARTS_FROM_EXE:
            self.set_cwd_if_started_from_exe()

        self.push_config_to_ui_boxes()

        self.setup_1st_tab()
        self.setup_2nd_tab()
        self.setup_3rd_tab()
        # print(config.CWD)
        # print(config.POST_NAME)
        # print(config.POST_OBJ)

    def push_config_to_ui_boxes(self):
        self.push_values_from_config_1_tab()
        self.push_values_from_config_2_tab()
        self.push_values_from_config_3_tab()

    def push_ui_boxes_to_config(self):
        self.write_values_from_1_tab_to_config()
        self.write_values_from_2_tab_to_config()
        self.write_values_from_3_tab_to_config()

    def setup_1st_tab(self):
        self.connect_buttons_1_tab()
        self.pushButton_tab1_confirm_changed_options.setEnabled(False)
        self.pushButton_tab1_discard_changed_options.setEnabled(False)
        self.pushButton_tab1_postprocess_start.setEnabled(False)
        self.comboBox_tab1_post_select.currentTextChanged.connect(self.write_values_from_1_tab_to_config)

    def setup_2nd_tab(self):
        self.connect_buttons_2_tab()

    def setup_3rd_tab(self):
        self.connect_buttons_3_tab()

    # VALUES FROM CONFIG
    def push_values_from_config_1_tab(self):
        logger.info("pushing values from config to 1 tab")
        self.comboBox_tab1_post_select.clear()
        self.comboBox_tab1_post_select.addItems(PostLister.post_dict.keys())
        self.comboBox_tab1_post_select.setCurrentText(config.POST_NAME)
        self.lineEdit_tab1_path_to_cwd.setText(config.abs_path_to_selected_file)

    def push_values_from_config_2_tab(self):
        logger.info("pushing values from config to 2 tab")
        self.checkBox_tab2_spindle_param_enabled.setChecked(config.G_CODE_SPINDLE_PARAMS_ENABLED)
        self.checkBox_tab2_feed_param_enabled.setChecked(config.G_CODE_FEED_PARAMS_ENABLED)
        self.checkBox_tab2_tool_param_enabled.setChecked(config.G_CODE_TOOL_POT_PARAMS_ENABLED)
        self.checkBox_tab2_g41g42_inverved.setChecked(config.G41_G42_SIDE_IS_REVERSED_SWITCH)
        self.checkBox_tab2_gather_massive_copies_enabled.setChecked(config.GATHER_MASSIVE_COPIES_AUTOMATICALLY)
        self.checkBox_tab2_gather_massive_copies_with_params_enabled.setChecked(
            config.GATHER_MASSIVE_COPIES_AUTOMATICALLY_VIA_PARAMS)

        self.lineEdit_tab2_spindle_param_text.setText(config.G_CODE_TOOL_RPM_PARAMETER)
        self.lineEdit_tab2_feed_param_text.setText(config.G_CODE_TOOL_FEED_PARAMETER)
        self.lineEdit_tab2_tool_param_text.setText(config.G_CODE_TOOL_POT_PARAMETER)
        self.lineEdit_tab2_main_letter_text.setText(config.PROGRAM_MAIN_LETTER)
        self.lineEdit_tab2_eob_text.setText(config.LINE_ENDING_EOB)

        self.textEdit_tab2_pprint_massive_copies_with_params.setText(config.PPRINT_FOR_GATHERING_VIA_PARAMS)
        self.spinBox_tab2_main_digit_text.setValue(int(config.PROGRAM_MAIN_DIGIT))

    def push_values_from_config_3_tab(self):
        logger.info("pushing values from config to 3 tab")
        self.checkBox_tab3_delete_temp_file.setChecked(config.DELETE_TEMP_FILE)

        self.lineEdit_tab3_temp_file_prefix.setText(config.TEMP_FILE_NAME_PREFIX)
        self.lineEdit_tab3_cl_file_extension.setText(config.CL_DATA_FILE_EXTENSION)
        self.lineEdit_tab3_gcode_file_extension.setText(config.G_CODE_FILE_EXTENSION)
        self.lineEdit_tab3_programmer_name.setText(config.PROGRAMMER_NAME)

    # VALUES TO CONFIG
    def write_values_from_1_tab_to_config(self):
        logger.info("writing values from boxes 1 tab to config")
        config.POST_NAME = self.comboBox_tab1_post_select.currentText()
        config.POST_OBJ = PostLister.post_dict[config.POST_NAME]
        # config.CWD = self.lineEdit_tab1_path_to_cwd.text()

        self.textEdit_tab1_log_output.append(f"Postprocessor selected: {config.POST_NAME}")

        # self.textEdit_tab1_log_output.append(f"Rewritten value: POST NAME to {config.POST_NAME}")
        # self.textEdit_tab1_log_output.append(f"Rewritten value: CWD to {config.CWD}")

    def write_values_from_2_tab_to_config(self):
        logger.info("writing values from boxes 2 tab to config")
        config.G_CODE_SPINDLE_PARAMS_ENABLED = self.checkBox_tab2_spindle_param_enabled.isChecked()
        config.G_CODE_FEED_PARAMS_ENABLED = self.checkBox_tab2_feed_param_enabled.isChecked()
        config.G_CODE_TOOL_POT_PARAMS_ENABLED = self.checkBox_tab2_tool_param_enabled.isChecked()
        config.G41_G42_SIDE_IS_REVERSED_SWITCH = self.checkBox_tab2_g41g42_inverved.isChecked()
        config.GATHER_MASSIVE_COPIES_AUTOMATICALLY = self.checkBox_tab2_gather_massive_copies_enabled.isChecked()
        config.GATHER_MASSIVE_COPIES_AUTOMATICALLY_VIA_PARAMS = self.checkBox_tab2_gather_massive_copies_with_params_enabled.isChecked()

        config.G_CODE_TOOL_RPM_PARAMETER = self.lineEdit_tab2_spindle_param_text.text()
        config.G_CODE_TOOL_FEED_PARAMETER = self.lineEdit_tab2_feed_param_text.text()
        config.G_CODE_TOOL_POT_PARAMETER = self.lineEdit_tab2_tool_param_text.text()
        config.PROGRAM_MAIN_LETTER = self.lineEdit_tab2_main_letter_text.text()
        config.LINE_ENDING_EOB = self.lineEdit_tab2_eob_text.text()

        config.PPRINT_FOR_GATHERING_VIA_PARAMS = self.textEdit_tab2_pprint_massive_copies_with_params.toPlainText()
        config.PROGRAM_MAIN_DIGIT = self.spinBox_tab2_main_digit_text.text()

        self.textEdit_tab1_log_output.append(f"Changes accepted for 2nd tab")

    def write_values_from_3_tab_to_config(self):
        logger.info("writing values from boxes 3 tab to config")
        config.DELETE_TEMP_FILE = self.checkBox_tab3_delete_temp_file.isChecked()
        config.TEMP_FILE_NAME_PREFIX = self.lineEdit_tab3_temp_file_prefix.text()
        config.CL_DATA_FILE_EXTENSION = self.lineEdit_tab3_cl_file_extension.text()
        config.G_CODE_FILE_EXTENSION = self.lineEdit_tab3_gcode_file_extension.text()
        config.PROGRAMMER_NAME = self.lineEdit_tab3_programmer_name.text()

        self.textEdit_tab1_log_output.append(f"Changes accepted for 3rd tab")

    # BUTTONS CONNECT
    def connect_buttons_1_tab(self):
        self.pushButton_tab1_postprocess_start.clicked.connect(self.btn_clicked_start_postprocess)
        self.pushButton_tab1_open_explorer.clicked.connect(self.open_file_explorer)
        self.pushButton_tab1_confirm_changed_options.clicked.connect(self.write_values_from_1_tab_to_config)
        self.pushButton_tab1_discard_changed_options.clicked.connect(self.discard_changed_options_tab1)

    def connect_buttons_2_tab(self):
        self.pushButton_tab2_confirm_changed_options.clicked.connect(self.write_values_from_2_tab_to_config)
        self.pushButton_tab2_discard_changed_options.clicked.connect(self.discard_changed_options_tab2)

    def connect_buttons_3_tab(self):
        self.pushButton_tab3_confirm_changed_settings.clicked.connect(self.write_values_from_3_tab_to_config)
        self.pushButton_tab3_discard_changed_settings.clicked.connect(self.discard_changed_options_tab3)

    def discard_changed_options_tab1(self):
        self.push_values_from_config_1_tab()
        self.textEdit_tab1_log_output.append(f"Changes declined for 1st tab")

    def discard_changed_options_tab2(self):
        self.push_values_from_config_2_tab()
        self.textEdit_tab1_log_output.append(f"Changes declined for 2nd tab")

    def discard_changed_options_tab3(self):
        self.push_values_from_config_3_tab()
        self.textEdit_tab1_log_output.append(f"Changes declined for 3rd tab")

    def set_cwd_if_started_from_project(self):
        if config.DEBUG:
            logger.debug("Setting cwd in debug mode")
            self.lineEdit_tab1_path_to_cwd.setText(config.DEBUG_CWD)
        else:
            pprint(sys.path)
            # path = sys.path[1]
            path = config.abs_path_to_selected_file
            self.lineEdit_tab1_path_to_cwd.setText(path)
            # config.work_ncl_file_path = path

    def set_cwd_if_started_from_exe(self):
        pprint(os.getcwd())
        path = os.getcwd()
        self.lineEdit_tab1_path_to_cwd.setText(path)
        config.abs_path_to_selected_file = path

    def open_file_explorer(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "NCL Files (*.ncl.*);;All Files (*);;",
            # "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
        )
        logger.debug(f"Filepath selected: {fname[0]}")
        self.textEdit_tab1_log_output.append(f"Filepath selected: {fname[0]}")
        if fname[0]:
            self.lineEdit_tab1_path_to_cwd.setText(fname[0])
            config.abs_path_to_selected_file = fname[0]
            self.pushButton_tab1_postprocess_start.setEnabled(True)

    def btn_clicked_start_postprocess(self):
        if config.POST_OBJ is None:
            self.textEdit_tab1_log_output.append(f"Select different POST")
        else:
            self.textEdit_tab1_log_output.append(f"postprocessing started")
            self.pushButton_tab1_postprocess_start.setEnabled(False)
            self.pushButton_tab1_postprocess_start.setText("Postprocessing . . .")
            is_executed = self.execute_postprocess(post_obj=config.POST_OBJ)
            if is_executed:
                self.textEdit_tab1_log_output.append(f"postprocessing finished")
            else:
                self.textEdit_tab1_log_output.append(f"postprocessing terminated with errors")

        self.pushButton_tab1_postprocess_start.setEnabled(True)
        self.pushButton_tab1_postprocess_start.setText("Запустить постпроцессирование")

    @staticmethod
    def execute_postprocess(post_obj) -> bool:
        if post_obj is None:
            logger.warning("Selected post is None")
            return False
        else:
            operations = list()

            filepath = config.abs_path_to_selected_file
            if filepath:
                operations.append(post_obj())
                for operation in operations:
                    operation.start_postprocessing()
                return True


def main_ui():
    app = QtWidgets.QApplication(sys.argv)
    window = DesktopWindowApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main_ui()
