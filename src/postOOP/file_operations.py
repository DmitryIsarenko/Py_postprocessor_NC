import os
from constants import (POST_NAME,
                       PROGRAMMER_NAME,
                       TEMP_FILE_NAME,
                       SAFETY_LINE_DEFAULT,
                       key_filename_part_1,
                       key_filename_part_2,)

from parsers.ncl_parser import parse_range_cl_records


def get_all_ncl_files_in_dir() -> list:
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




def read_ncl_file_format_and_create_temp_file(filepath: str):
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



def create_files_for_ustanov(pprint_vars: dict) -> None:
    with open(file=pprint_vars["ust_O_name_with_extension"], mode="w") as ust_head_file:
        ust_head_file.write(f"(POSTPROCESSED BY : {POST_NAME});\n"
                            f"(PROGRAMMER : {PROGRAMMER_NAME});\n"
                            f"(DATE : {pprint_vars["date_and_time"]});\n"
                            f"(PART NUMBER : {pprint_vars["part_name"]});\n"
                            f"(USTANOV NUMBER : {pprint_vars["ust_num_str"]});\n"
                            f";\n")

    print(f"ustanov file №{pprint_vars["ust_num_str"]} has been created")

    for sub_program_dict in pprint_vars["operations"]:
        with open(file=pprint_vars["ust_O_name_with_extension"], mode="a") as ust_head_file:
            ust_head_file.write(
                f"M98P{sub_program_dict["program_O_name"][1::1]}({sub_program_dict["operation_name"]} - "
                f"PROGRAM NUMBER : {sub_program_dict["program_num_str"]} / {len(pprint_vars["operations"])});\n"
                f"(T{sub_program_dict["tool_pot_num_str"]} - {sub_program_dict["tool_name"]});\n"

                f";\n")

    with open(file=pprint_vars["ust_O_name_with_extension"], mode="a") as ust_head_file:
        ust_head_file.write(f"G0 G53 Z0.;\n"
                            f"G0 X0.;\n"
                            f"G53 Y0.;\n"
                            f";\n"
                            f"(MACHINING TIME : {pprint_vars["sum_machining_time"]});")


def create_files_for_operations_in_ustanov(pprint_vars: dict) -> None:
    for sub_program_dict_index in range(len(pprint_vars["operations"])):
        prog_physical_num = sub_program_dict_index + 1

        print(f"started creating {prog_physical_num} subprogram")

        ust_sub_prog_name = pprint_vars["operations"][sub_program_dict_index]["program_O_name"]
        with open(file=ust_sub_prog_name, mode="w") as sub_prog:
            sub_prog.write(f"(POSTPROCESSED BY : {POST_NAME});\n"
                           f"(PROGRAMMER : {PROGRAMMER_NAME});\n"
                           f"(DATE : {pprint_vars["date_and_time"]});\n"
                           f"(PART NUMBER : {pprint_vars["part_name"]});\n"
                           f"(USTANOV NUMBER : {pprint_vars["ust_num_str"]});\n"
                           f"(PROGRAM NUMBER : {prog_physical_num} / {len(pprint_vars["operations"])});\n"
                           f"(PROGRAM NAME : {pprint_vars["operations"][prog_physical_num - 1]["operation_name"]});\n"
                           f";\n"
                           f"{SAFETY_LINE_DEFAULT};\n"
                           f"")


def loop_through_all_subprograms_parsing_range_cl_lines(cl_lines, pprint_vars: dict) -> None:
    for sub_prog_dict in pprint_vars["operations"]:
        result_list = parse_range_cl_records(cl_lines=cl_lines,
                                             pprint_vars=pprint_vars,
                                             program_num_iter=sub_prog_dict["program_num_iter"])
        append_parsed_lines_to_file(file_to_open=sub_prog_dict["program_O_name_with_extension"],
                                    list_with_lines=result_list)


def append_parsed_lines_to_file(file_to_open: str, list_with_lines: list[str]):
    with open(file=file_to_open, mode="a") as file:
        for line in list_with_lines:
            file.write(line)


def remove_temp_file():
    if os.path.exists(TEMP_FILE_NAME):
        os.remove(path=TEMP_FILE_NAME)
        print()
    else:
        print("no temp file was found")
