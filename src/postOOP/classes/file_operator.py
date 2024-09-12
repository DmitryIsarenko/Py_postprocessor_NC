import os
from src.postOOP.config import TEMP_FILE_NAME, key_filename_part_2


class FileOperator():

    @staticmethod
    def get_all_ncl_files_in_dir() -> list:
        lst = os.listdir()
        # unic_files = set(file for file in lst if key_filename_part_1 in file[:4] and key_filename_part_2 in file)
        unic_files = set(file for file in lst if key_filename_part_2 in file)
        final_filenames = set()
        for basic_filename in unic_files:
            temp_list = [basic_filename, ]
            for repeating_name in unic_files:
                if basic_filename[:-2:] == repeating_name[:-2:]:
                    temp_list.append(repeating_name)
                else:
                    continue
            final_filenames.add(max(temp_list))
        print(f"Found files to postprocess: {sorted(final_filenames)}")
        return sorted(final_filenames)

    @staticmethod
    def append_parsed_lines_to_file(filepath: str, list_with_lines: list[str]):
        with open(file=filepath, mode="a") as file:
            for line in list_with_lines:
                file.write(line)

    @staticmethod
    def remove_file(filepath: str) -> bool:
        if os.path.exists(filepath):
            os.remove(path=filepath)
            return True
        else:
            print("no temp file was found")
            return False

    @staticmethod
    def create_temp_formatted_ncl_file(filepath: str, temp_filepath: str = None) -> str:
        if temp_filepath is None:
            temp_filepath = f"temp_{filepath}"

        with open(file=filepath, mode="r") as ncl_file:
            lines = ncl_file.readlines()
            for line_index in range(lines.__len__()):
                if lines[line_index][-2] == "$":
                    lines[line_index] = lines[line_index].replace("$\n", "").strip()
        print(f'.ncl file "{filepath}" has been read')
        with open(file=temp_filepath, mode="w") as temp_file:
            temp_file.writelines(lines)
        return temp_filepath

    @staticmethod
    def get_cl_lines_in_range(filepath: str, start_index: int = 0, end_index: int = -1) -> list[str]:
        with open(file=filepath, mode="r") as file:
            list_of_cl_lines = file.readlines()[start_index:end_index:1]
        return list_of_cl_lines
