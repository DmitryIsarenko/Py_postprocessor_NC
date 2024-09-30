from pprint import pprint
from src.postOOP import config

class NcProgram:
    main_digit = config.PROGRAM_MAIN_DIGIT
    main_letter = config.PROGRAM_MAIN_LETTER
    file_extension = config.G_CODE_FILE_EXTENSION
    postprocessor_name = config.POST_NAME
    programmer_name = config.PROGRAMMER_NAME

    cl_list: list[str] = []
    nc_list: list[str] = []

    def show(self):
        print(f"\n\n"
              f"Dictionary of {self.__class__} object")
        pprint(self.__dict__)
        print(f"\n\n")
