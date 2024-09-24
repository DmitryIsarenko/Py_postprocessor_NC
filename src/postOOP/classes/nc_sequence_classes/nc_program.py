from pprint import pprint
from src.postOOP.config import (PROGRAM_MAIN_DIGIT,
                                PROGRAM_MAIN_LETTER,
                                G_CODE_FILE_EXTENSION,
                                POST_NAME,
                                PROGRAMMER_NAME,
                                )


class NcProgram:
    main_digit = PROGRAM_MAIN_DIGIT
    main_letter = PROGRAM_MAIN_LETTER
    file_extension = G_CODE_FILE_EXTENSION
    postprocessor_name = POST_NAME
    programmer_name = PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []

    def show(self):
        print(f"\n\n"
              f"Dictionary of {self.__class__} object")
        pprint(self.__dict__)
        print(f"\n\n")
