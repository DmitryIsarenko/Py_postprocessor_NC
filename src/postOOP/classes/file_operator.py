import os
from src.postOOP.constants import TEMP_FILE_NAME


class FileOperator():

    def append_parsed_lines_to_file(self, file_to_open: str, list_with_lines: list[str]):
        with open(file=file_to_open, mode="a") as file:
            for line in list_with_lines:
                file.write(line)

    def remove_temp_file(self):
        if os.path.exists(TEMP_FILE_NAME):
            os.remove(path=TEMP_FILE_NAME)
            print()
        else:
            print("no temp file was found")
