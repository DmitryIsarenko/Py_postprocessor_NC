from pprint import pprint

from src.postOOP.constants import (PROGRAM_PREFIX,
                                   PROGRAM_MAIN_DIGIT,
                                   G_CODE_FILE_EXTENSION,
                       # G_CODE_PARAMS_ENABLED,
                                   G_CODE_FEED_PARAMS_ENABLED,
                                   G_CODE_SPINDLE_PARAMS_ENABLED,
                                   G_CODE_TOOL_POT_PARAMS_ENABLED,
                                   G_CODE_TOOL_FEED_PARAMETER,
                                   G_CODE_TOOL_RPM_PARAMETER,
                                   G_CODE_TOOL_POT_PARAMETER,
                                   G41_G42_SIDE_IS_REVERSED_SWITCH,
                                   dict_of_axial_operations_G_codes, )

class NclParser():

    def parse_range_cl_records(self, cl_lines: list, program_num_iter: int, pprint_vars: dict) -> list[str]:
        result_list = []
        start_cl_line = pprint_vars["operations"][program_num_iter]["cl_line_index_start"]
        end_cl_line = pprint_vars["operations"][program_num_iter]["cl_line_index_end"]

        for line_index in range(start_cl_line, end_cl_line):

            if "PPRINT /" in cl_lines[line_index]:
                pass
            elif "UNITS /" in cl_lines[line_index]:
                units_str = cl_lines[line_index].split(sep=" / ")[1]
                if units_str == "MM":
                    result_list.append("G21")
                elif units_str == "INCH":
                    result_list.append("G20")
                else:
                    result_list.append("UNKNOWN UNITS")

            elif "SET / OFSETL, " in cl_lines[line_index]:
                right_part = cl_lines[line_index].split(sep=", ")[1].strip()
                if "OFF" in right_part:
                    result_list.append("G28 Z0 G49;\n")
                elif int(float(right_part)).is_integer():
                    result_list.append(f"G{right_part};\n")

            elif "CSYS /" in cl_lines[line_index]:
                pass
                right_part_str = cl_lines[line_index].split(sep=" / ")[1]
                right_part_list = right_part_str.split(sep=",")
                csys_coords = [round(float(char), ndigits=5) for char in right_part_list]

            elif "LOADTL /" in cl_lines[line_index]:
                result_list.append(f"(TOOL NAME: {pprint_vars["operations"][program_num_iter]["tool_name"]});\n", )




                if G_CODE_TOOL_POT_PARAMS_ENABLED == 0:
                    result_list.append(f"T{pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]} M6;\n", )
                    pass
                elif G_CODE_TOOL_POT_PARAMS_ENABLED == 1:
                    result_list.append(
                        f"{G_CODE_TOOL_POT_PARAMETER}={pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]}"
                        f"(NOMER T INSTRUMENTA);\n", )
                    pass

                if G_CODE_SPINDLE_PARAMS_ENABLED == 0:
                    pass
                elif G_CODE_SPINDLE_PARAMS_ENABLED == 1:
                    result_list.append(f"{G_CODE_TOOL_RPM_PARAMETER}="
                                       f"{pprint_vars["operations"][program_num_iter]["spindle_speed"]}"
                                       f"(OBOROTI);\n")
                    pass

                if G_CODE_FEED_PARAMS_ENABLED == 0:
                    pass
                elif G_CODE_FEED_PARAMS_ENABLED == 1 and pprint_vars["operations"][program_num_iter][
                    "cut_feed"] != "null":
                    result_list.append(
                        f"{G_CODE_TOOL_FEED_PARAMETER}={pprint_vars["operations"][program_num_iter]["cut_feed"]}"
                        f"(PODACHA);\n")
                    # result_list.append(f";\n", )
                    # result_list.append(f"T{G_CODE_TOOL_POT_PARAMETER} M6;\n", )






                # if G_CODE_PARAMS_ENABLED == 0 or (G_CODE_PARAMS_ENABLED == 1 and G_CODE_TOOL_POT_PARAMS_ENABLED == 0):
                #     result_list.append(f"T{pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]} M6;\n", )
                # elif G_CODE_PARAMS_ENABLED == 1:
                #     if G_CODE_TOOL_POT_PARAMS_ENABLED == 1:
                #         result_list.append(
                #             f"{G_CODE_TOOL_POT_PARAMETER}={pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]}"
                #             f"(NOMER T INSTRUMENTA);\n", )
                # if G_CODE_SPINDLE_PARAMS_ENABLED == 1:
                #     result_list.append(f"{G_CODE_TOOL_RPM_PARAMETER}="
                #                        f"{pprint_vars["operations"][program_num_iter]["spindle_speed"]}"
                #                        f"(OBOROTI);\n")
                # if G_CODE_FEED_PARAMS_ENABLED == 1 and pprint_vars["operations"][program_num_iter][
                #     "cut_feed"] != "null":
                #     result_list.append(
                #         f"{G_CODE_TOOL_FEED_PARAMETER}={pprint_vars["operations"][program_num_iter]["cut_feed"]}"
                #         f"(PODACHA);\n")
                #     result_list.append(f";\n", )
                #     result_list.append(f"T{G_CODE_TOOL_POT_PARAMETER} M6;\n", )







            elif "SPINDL /" in cl_lines[line_index]:
                right_part = cl_lines[line_index].split(sep=" / ")[1].strip()
                if "OFF" in right_part:
                    result_list.append("M05;\n")
                elif "RPM, " in right_part:
                    right_part_list = right_part.split(sep=",")
                    right_part_list = [item.strip() for item in right_part_list]
                    for item in right_part_list:
                        if item == "RPM":
                            result_list.append("G97 ")
                        elif item == "CLW":
                            result_list.append("M03")
                        elif item == "CCLW":
                            result_list.append("M04")
                        else:
                            if G_CODE_SPINDLE_PARAMS_ENABLED == 0:
                                item = round(float(item))
                                result_list.append(f"S{item} ")
                            elif G_CODE_SPINDLE_PARAMS_ENABLED == 1:
                                result_list.append(f"S{G_CODE_TOOL_RPM_PARAMETER} ")
                            # if G_CODE_PARAMS_ENABLED == 0 or (G_CODE_PARAMS_ENABLED == 1 and G_CODE_SPINDLE_PARAMS_ENABLED == 0):
                            #     item = round(float(item))
                            #     result_list.append(f"S{item} ")
                            # elif G_CODE_PARAMS_ENABLED == 1 and G_CODE_SPINDLE_PARAMS_ENABLED == 1:
                            #     result_list.append(f"S{G_CODE_TOOL_RPM_PARAMETER} ")
                    result_list.append(";\n")








            elif "COOLNT /" in cl_lines[line_index]:
                right_part = cl_lines[line_index].split(sep=" / ")[1]
                if "ON" in right_part:
                    result_list.append(f"M08;\n")
                elif "OFF" in right_part:
                    result_list.append(f"M09;\n")


            elif "FEDRAT / " in cl_lines[line_index]:
                if G_CODE_FEED_PARAMS_ENABLED == 0:
                    right_part_list = cl_lines[line_index].split(sep=" / ")[1].strip().split(sep=",")
                    feedrate = round(float(right_part_list[0]), ndigits=2)
                    result_list.append(f"G01 F{feedrate} ")
                elif G_CODE_FEED_PARAMS_ENABLED == 1:
                    result_list.append(f"G01 F{G_CODE_TOOL_FEED_PARAMETER} ")
                # elif G_CODE_PARAMS_ENABLED == 1 and G_CODE_FEED_PARAMS_ENABLED == 1:
                #     result_list.append(f"G01 F{G_CODE_TOOL_FEED_PARAMETER} ")


            elif "CUTCOM / " in cl_lines[line_index]:
                cutcom_str = cl_lines[line_index].split(sep=" / ")[1].strip()
                if G41_G42_SIDE_IS_REVERSED_SWITCH == 0:
                    left_compensation = "G41"
                    right_compensation = "G42"
                else:  # G41_G42_SIDE_IS_REVERSED_SWITCH == 1
                    left_compensation = "G42"
                    right_compensation = "G41"










                if G_CODE_TOOL_POT_PARAMS_ENABLED == 0:
                    D_corrector_addition = f"D{pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]}"
                elif G_CODE_TOOL_POT_PARAMS_ENABLED == 1:
                    D_corrector_addition = f"D{G_CODE_TOOL_POT_PARAMETER}"
                # if G_CODE_PARAMS_ENABLED == 0 or (G_CODE_PARAMS_ENABLED == 1 and G_CODE_TOOL_POT_PARAMS_ENABLED == 0):
                #     D_corrector_addition = f"D{pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]}"
                # elif G_CODE_PARAMS_ENABLED == 1 and G_CODE_TOOL_POT_PARAMS_ENABLED == 1:
                #     D_corrector_addition = f"D{G_CODE_TOOL_POT_PARAMETER}"









                if cutcom_str == "OFF":
                    result_list.append(f"G40 ")
                elif cutcom_str == "LEFT":
                    result_list.append(f"{left_compensation} {D_corrector_addition} ")
                elif cutcom_str == "RIGHT":
                    result_list.append(f"{right_compensation} {D_corrector_addition} ")


















            elif "GOTO / " in cl_lines[line_index]:
                if not ("CIRCLE" in cl_lines[line_index - 1] and "CIRCLE" in cl_lines[line_index + 1]):
                    if "CIRCLE" in cl_lines[line_index - 1]:
                        result_list.append(f"G01 ")

                    right_part_list = cl_lines[line_index].split(sep=" / ")[1].strip().split(sep=",")
                    right_part_list = [round(float(item), ndigits=5) for item in right_part_list]

                    if len(right_part_list) == 3:
                        x, y, z = right_part_list
                        result_list.append(f"X{x} Y{y} Z{z};\n")

                    elif len(right_part_list) == 6:
                        pass
                    else:
                        print("error with num of scalars")

            elif "RAPID" in cl_lines[line_index]:
                result_list.append(f"G00 ")

            elif "CIRCLE / " in cl_lines[line_index]:
                prev_coords_list_str = cl_lines[line_index - 1].split(sep=" / ")[1].strip().split(sep=",")
                prev_coords_list_float = [round(float(item), ndigits=5) for item in prev_coords_list_str]
                x_start_abs, y_start_abs, z_start_abs = prev_coords_list_float

                right_part_list = cl_lines[line_index].split(sep=" / ")[1].strip().split(sep=",")
                right_part_list_float = [round(float(item), ndigits=5) for item in right_part_list]

                end_coords = cl_lines[line_index + 1].split(sep=" / ")[1].strip().split(sep=",")
                end_coords_float = [round(float(item), ndigits=5) for item in end_coords]
                x_end_abs, y_end_abs, z_end_abs = end_coords_float

                (x_center_abs, y_center_abs, z_center_abs,
                 csys_vector_i, csys_vector_j, csys_vector_k, radius) = right_part_list_float

                x_center_incr = round(x_center_abs - x_start_abs, ndigits=5)
                y_center_incr = round(y_center_abs - y_start_abs, ndigits=5)
                z_center_incr = round(z_center_abs - z_start_abs, ndigits=5)

                if csys_vector_k == -1:
                    result_list.append("G02 ")
                elif csys_vector_k == 1:
                    result_list.append("G03 ")

                result_list.append(f"X{x_end_abs} "
                                   f"Y{y_end_abs} "
                                   f"Z{z_end_abs} "
                                   f"I{x_center_incr} "
                                   f"J{y_center_incr} "
                                   f"K{z_center_incr}"
                                   # f"R{radius}"
                                   )
                result_list.append(f";\n")

            elif "CYCLE /" in cl_lines[line_index]:
                right_part_list = cl_lines[line_index].split(sep=" / ")[1].strip().split(sep=", ")

                operation_data: dict = {
                    "OPERATION_CODE": None,
                    "DEPTH": None,
                    "STEP": None,
                    "ZFEED": None,
                    "FEED_TYPE": None,  # MMPM or MMPR
                    "FEED_RATE": None,
                    "CLEAR": None,
                    "RETURN": None,
                }

                if "OFF" in right_part_list:
                    result_list.append("G80;\n", )
                elif right_part_list[  # если имя операции из перечня ключей словаря с типами операций
                    0] in dict_of_axial_operations_G_codes.keys():
                    result_list.append(f"G98 ")
                    result_list.append(dict_of_axial_operations_G_codes[right_part_list[0]] + " ")










                    if "MMPM" in right_part_list:
                        operation_data["FEED_TYPE"] = "G94"
                        feed_type_index = right_part_list.index("MMPM")
                        operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]), ndigits=4)
                        if G_CODE_FEED_PARAMS_ENABLED == 0 or pprint_vars["operations"][program_num_iter]["cut_feed"] == "null":
                            result_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                        elif G_CODE_FEED_PARAMS_ENABLED == 1:
                            result_list.append(f"{operation_data["FEED_TYPE"]} F{G_CODE_TOOL_FEED_PARAMETER} ")
                        # if (G_CODE_PARAMS_ENABLED == 0 or
                        #     pprint_vars["operations"][program_num_iter]["cut_feed"] == "null") or (
                        #         G_CODE_PARAMS_ENABLED == 1 and G_CODE_FEED_PARAMS_ENABLED == 0):
                        #     result_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                        # elif G_CODE_FEED_PARAMS_ENABLED == 1 and G_CODE_PARAMS_ENABLED == 1:
                        #     result_list.append(f"{operation_data["FEED_TYPE"]} F{G_CODE_TOOL_FEED_PARAMETER} ")









                    elif "MMPR" in right_part_list:
                        operation_data["FEED_TYPE"] = "G95"
                        feed_type_index = right_part_list.index("MMPR")
                        operation_data["FEED_RATE"] = round(float(right_part_list[feed_type_index + 1]), ndigits=4)
                        if G_CODE_FEED_PARAMS_ENABLED == 0 or pprint_vars["operations"][program_num_iter]["cut_feed"] == "null":
                            result_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                        elif G_CODE_FEED_PARAMS_ENABLED == 1:
                            result_list.append(f"{operation_data["FEED_TYPE"]} F{G_CODE_TOOL_FEED_PARAMETER} ")
                        # if G_CODE_FEED_PARAMS_ENABLED == 0 or pprint_vars["operations"][program_num_iter]["cut_feed"] == "null":
                        #     result_list.append(f"{operation_data["FEED_TYPE"]} F{operation_data["FEED_RATE"]} ")
                        # elif G_CODE_FEED_PARAMS_ENABLED == 1:
                        #     result_list.append(f"{operation_data["FEED_TYPE"]} F{G_CODE_TOOL_FEED_PARAMETER} ")









                    if "DEPTH" in right_part_list:
                        depth_index = right_part_list.index("DEPTH")
                        operation_data["DEPTH"] = round(float(right_part_list[depth_index + 1]), ndigits=5)
                        result_list.append(f"Z{operation_data["DEPTH"]} ")
                    if "STEP" in right_part_list:
                        step_index = right_part_list.index("STEP")
                        operation_data["STEP"] = round(float(right_part_list[step_index + 1]), ndigits=5)
                        result_list.append(f"Q{operation_data["STEP"]} ")
                    if "CLEAR" in right_part_list:
                        clear_index = right_part_list.index("CLEAR")
                        operation_data["CLEAR"] = round(float(right_part_list[clear_index + 1]), ndigits=5)
                        result_list.append(f"R{operation_data["CLEAR"]} ")
                    if "ZFEED" in right_part_list:
                        zfeed_index = right_part_list.index("ZFEED")
                        operation_data["ZFEED"] = round(float(right_part_list[zfeed_index + 1]), ndigits=4)
                    result_list.append(f";\n")

            elif "END /" in cl_lines[line_index]:
                result_list.append("M01;\n", )
                result_list.append("M99;\n", )
                result_list.append(f";\n")

            elif "FINI" in cl_lines[line_index]:
                result_list.pop()
                result_list.append(f"M30;\n")
                result_list.append(f";")

            elif "$$" in cl_lines[line_index]:
                pass
            else:
                print(f"HAVENT PARSED cl record: {cl_lines[line_index]}")







        # adding G43 compensation to the 1st GOTO
        counter_lines_with_z = 0
        for line_index in range(len(result_list)):
            line = result_list[line_index]
            if "G00" in line or "G01" in line:
                counter_lines_with_z += 1
                if counter_lines_with_z > 0:
                    if G_CODE_TOOL_POT_PARAMS_ENABLED == 0:
                        insertion = f"G43 H{pprint_vars["operations"][program_num_iter]["tool_pot_num_str"]} "
                    elif G_CODE_TOOL_POT_PARAMS_ENABLED == 1:  # G_CODE_PARAMS_ENABLED == 1:
                        insertion = f"G43 H{G_CODE_TOOL_POT_PARAMETER} "
                    result_list[line_index] = insertion + result_list[line_index]
                    break
                else:
                    continue
            else:
                continue
        return result_list
