from src.postOOP.config import PROGRAM_MAIN_LETTER, PROGRAM_MAIN_DIGIT, G_CODE_FILE_EXTENSION, POST_NAME, PROGRAMMER_NAME




class GCodeFile:
    extension = G_CODE_FILE_EXTENSION
    prefix = PROGRAM_MAIN_LETTER
    main_digit = PROGRAM_MAIN_DIGIT


class UstanovFileCreator(GCodeFile):
    def create_files_for_ustanov(self, pprint_vars: dict) -> None:
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


class ProgramFile(GCodeFile):
    pass


class ProgramFile3AxisMill(ProgramFile):
    pass


class ProgramFile4AxisAMill(ProgramFile):
    pass
