from pprint import pprint

from ..constants import (PROGRAM_PREFIX,
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



def parse_pprint(lines) -> dict:
    print("Parsing PPRINTs")
    pprint_vars = {
        "part_name": "null",
        "date_and_time": "null",
        "ust_name": "null",
        "ust_num_str": "null",
        "ust_O_name": "null",
        "ust_O_name_with_extension": "null",
        "operations": [],
        "cl_file_lines": lines.__len__(),
        "sum_machining_time": 0,
    }
    program_counter = 0

    for line_index in range(lines.__len__()):
        cl_line = lines[line_index]
        if "PPRINT" in cl_line:
            if "PART NAME" in cl_line:
                pprint_vars["part_name"] = cl_line.split(sep=" : ")[1][:-1:]
            elif "DATE TIME" in cl_line:
                pprint_vars["date_and_time"] = cl_line.split(sep=" : ")[1][:-1:]
            elif "OPERATION NAME" in cl_line:
                pprint_vars["ust_name"] = cl_line.split(sep=" : ")[1][:-1:]

                ust_num_str = ""

                for char in pprint_vars["ust_name"]:
                    if char.isdigit():
                        ust_num_str += str(char)
                pprint_vars["ust_num_str"] = ust_num_str
                ust_O_name = PROGRAM_PREFIX + PROGRAM_MAIN_DIGIT + ust_num_str + "00"
                pprint_vars["ust_O_name"] = ust_O_name
                pprint_vars["ust_O_name_with_extension"] = ust_O_name + G_CODE_FILE_EXTENSION

            elif "NC SEQUENCE NAME" in cl_line:
                program_counter += 1

                operation_template_dict = {
                    "cl_line_index_start": "null",
                    "cl_line_index_end": "null",
                    "pprints_index_start": "null",
                    "pprints_index_end": "null",
                    "operation_name": "null",
                    "machining_time": 0,
                    "tool_name": "null",
                    "program_num_iter": "null",
                    "program_num": "null",
                    "program_num_str": "null",
                    "program_O_name": "null",
                    "program_O_name_with_extension": "null",
                    "tool_pot_num_str": "null",
                    "cut_feed": "null",
                    "spindle_speed": "null",
                }

                pprint_counter = 1
                while "LOADTL" not in lines[line_index + pprint_counter]:
                    pprint_counter += 1

                cl_in_prog_counter = 1
                while "$$-> END /" not in lines[line_index + cl_in_prog_counter]:
                    cl_in_prog_counter += 1

                operation_template_dict["pprints_index_start"] = line_index
                operation_template_dict["pprints_index_end"] = line_index + pprint_counter
                operation_template_dict["cl_line_index_start"] = line_index
                operation_template_dict["cl_line_index_end"] = line_index + cl_in_prog_counter + 1

                operation_template_dict["program_num"] = program_counter
                operation_template_dict["program_num_iter"] = program_counter - 1

                for sub_line_index in range(line_index, line_index + pprint_counter + 1):
                    sub_cl_line = lines[sub_line_index]

                    if "NC SEQUENCE NAME" in sub_cl_line:
                        operation_template_dict["operation_name"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                        # operation_template_dict["cl_line_index_start"] = sub_line_index
                    elif "MACHINING TIME" in sub_cl_line:
                        operation_template_dict["machining_time"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                    elif "TOOL NAME" in sub_cl_line:
                        operation_template_dict["tool_name"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                    elif "SPINDLE SPEED" in sub_cl_line:
                        operation_template_dict["spindle_speed"] = round(
                            float(sub_cl_line.split(sep=" : ")[1][:-1:].split(sep=" ")[0]), ndigits=2)
                    elif "CUT_FEED" in sub_cl_line:
                        operation_template_dict["cut_feed"] = round(float(sub_cl_line.split(sep=" : ")[1][:-1:]),
                                                                    ndigits=2)
                    elif "LOADTL" in sub_cl_line:
                        right_part = sub_cl_line.split(sep=" / ")[1][:-1:]
                        if "$$->" in right_part:
                            pot_num = right_part.split(sep=" $$-> ")[0]
                            operation_template_dict["tool_pot_num_str"] = pot_num
                        else:
                            operation_template_dict["tool_pot_num_str"] = sub_cl_line.split(sep=" / ")[1][:-1:]

                    if program_counter < 10:
                        operation_template_dict["program_num_str"] = "0" + str(program_counter)
                    elif 10 <= program_counter < 100:
                        operation_template_dict["program_num_str"] = str(program_counter)

                    ust_sub_prog_name = PROGRAM_PREFIX + PROGRAM_MAIN_DIGIT + pprint_vars["ust_num_str"] + \
                                        operation_template_dict["program_num_str"]

                    operation_template_dict["program_O_name"] = ust_sub_prog_name
                    operation_template_dict["program_O_name_with_extension"] = ust_sub_prog_name + G_CODE_FILE_EXTENSION

                pprint_vars["operations"].append(operation_template_dict)

            else:
                continue
        else:
            continue

    sum_machining_time = 0
    for operation_dict in pprint_vars["operations"]:
        sum_machining_time += float(operation_dict["machining_time"])
    pprint_vars["sum_machining_time"] = round(sum_machining_time, 2)

    pprint(pprint_vars)
    return pprint_vars
