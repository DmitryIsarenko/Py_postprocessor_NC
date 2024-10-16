import os
import logging
# from src.postOOP.config import config.TEMP_FILE_NAME_PREFIX, config.CL_DATA_FILE_EXTENSION
from src.postOOP.classes.others.formatter import Formatter

from src.postOOP import config

logger = logging.getLogger(__name__)

class FileOperatorBasic:

    @staticmethod
    def get_all_ncl_files_in_dir(path: str) -> list[str] | None:

        # os.chdir("../../../../../")
        # os.chdir("../../../")
        # os.chdir("../../")
        os.chdir(path=path)
        lst = os.listdir()
        logger.info(f"Files found in cwd: {lst}")

        unic_files = set(file for file in lst if config.CL_DATA_FILE_EXTENSION in file)
        if unic_files:
            final_filenames = set()
            for basic_filename in unic_files:
                temp_list = [basic_filename, ]
                for repeating_name in unic_files:
                    if basic_filename[:-2:] == repeating_name[:-2:]:
                        temp_list.append(repeating_name)
                    else:
                        continue
                final_filenames.add(max(temp_list))
            # print(f"Found files to postprocess: {sorted(final_filenames)}")
            return sorted(final_filenames)
        else:
            logger.info(f"No files with '{config.CL_DATA_FILE_EXTENSION}' extension were found")
            return None

    @staticmethod
    def append_lines_to_file(filepath: str, list_with_lines: list[str]):
        with open(file=filepath, mode="w") as file:
            for line in list_with_lines:
                file.write(line)

    @staticmethod
    def remove_file(*, filepath: str) -> bool:
        try:
            # os.remove(path="".join([filepath, r"/.."]))
            os.remove(path=filepath)
            return True
        except FileNotFoundError:
            logger.info("no temp file was found")
            return False
        except TypeError:
            return False

    @classmethod
    def create_temp_formatted_ncl_file(cls, *, temp_filepath: str = None) -> str | None:
        if temp_filepath is None:
            temp_filepath = f"{config.work_ncl_file_path}/../{config.TEMP_FILE_NAME_PREFIX}{config.CL_DATA_FILE_EXTENSION}.1"
        FileOperatorBasic.remove_file(filepath=temp_filepath)
        lines = cls.get_all_cl_lines(filepath=config.work_ncl_file_path)
        lines = Formatter.trim_line_connectors_in_cl_list(cl_list=lines)
        logger.info(f'.ncl file "{config.work_ncl_file_path}" has been read')
        cls.append_lines_to_file(filepath=temp_filepath, list_with_lines=lines)
        return temp_filepath

    @staticmethod
    def check_if_file_is_present(*, filepath: str) -> bool:
        if filepath and os.path.exists(filepath):
            return True
        else:
            return False

    @classmethod
    def get_cl_lines_in_range(cls, *, filepath: str, start_index: int = 0, end_index: int) -> list[str] | None:
        if cls.check_if_file_is_present(filepath=filepath):
            with open(file=filepath, mode="r") as file:
                list_of_cl_lines = file.readlines()[start_index:end_index:1]
            return list_of_cl_lines
        else:
            return None

    @classmethod
    def get_all_cl_lines(cls, *, filepath: str) -> list[str] | None:
        if cls.check_if_file_is_present(filepath=filepath):
            with open(file=filepath, mode="r") as file:
                list_of_cl_lines = file.readlines()[0::1]
            return list_of_cl_lines
        else:
            return None

    @classmethod
    def create_file(cls, *, filepath: str) -> None:
        if cls.check_if_file_is_present(filepath=filepath):
            cls.remove_file(filepath=filepath)
        with open(file=filepath, mode="w"):
            logger.info(f"created file '{filepath}'")
