from src.postOOP.constants import POST_NAME, PROGRAMMER_NAME, SAFETY_LINE_DEFAULT

class ProgramFileCreator():
    def create_files_for_operations_in_ustanov(self, pprint_vars: dict) -> None:
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

