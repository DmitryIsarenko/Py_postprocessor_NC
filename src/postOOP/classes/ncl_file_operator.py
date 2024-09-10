import os
from src.postOOP.constants import key_filename_part_1, key_filename_part_2
class NclFileOperator():
    def get_all_ncl_files_in_dir(self) -> list:
        lst = os.listdir()
        unic_files = set(file for file in lst if key_filename_part_1 in file[:4] and key_filename_part_2 in file)
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

    def read_ncl_file_format_and_create_temp_file(self, filepath: str):
        with open(file=filepath, mode="r") as ncl_file:
            lines = ncl_file.readlines()
            for line_index in range(lines.__len__()):
                if lines[line_index][-2] == "$":
                    lines[line_index] = lines[line_index].replace("$\n", "").strip()
        print(f'.ncl file "{filepath}" has been read')
        with open(file="temp.txt", mode="w") as temp_file:
            temp_file.writelines(lines)
        with open(file="temp.txt", mode="r") as temp_file:
            lines = temp_file.readlines()
        return lines