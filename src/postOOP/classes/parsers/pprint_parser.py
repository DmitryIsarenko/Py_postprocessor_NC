from pprint import pprint

from src.postOOP.config import (PROGRAM_PREFIX,
                                PROGRAM_MAIN_DIGIT,
                                G_CODE_FILE_EXTENSION,
                                ust_template_dict,
                                operation_template_dict)


class PprintParser():
    program_counter = 0
    @staticmethod
    def get_cl_file_lines_amount(lines):
        return lines.__len__()

    @staticmethod
    def sum_machining_time(*, pprint_vars):
        sum_machining_time = 0
        for operation_dict in pprint_vars["operations"]:
            sum_machining_time += float(operation_dict["machining_time"])
        return round(sum_machining_time, ndigits=2)

    @staticmethod
    def get_cl_part_after_colon(*, cl_line):
        return cl_line.split(sep=" : ")[1][:-1:]

    @classmethod
    def get_part_name(cls, *, cl_line):
        return cls.get_cl_part_after_colon(cl_line=cl_line)

    @classmethod
    def get_date_and_time(cls, *, cl_line):
        return cls.get_cl_part_after_colon(cl_line=cl_line)

    @classmethod
    def write_ust_name_and_sub_data(cls, *, pprint_vars, cl_line):
        pprint_vars["ust_name"] = cls.get_cl_part_after_colon(cl_line=cl_line)

        ust_num_str = ""

        for char in pprint_vars["ust_name"]:
            if char.isdigit():
                ust_num_str += str(char)
        pprint_vars["ust_num_str"] = ust_num_str
        ust_O_name = PROGRAM_PREFIX + PROGRAM_MAIN_DIGIT + ust_num_str + "00"
        pprint_vars["ust_O_name"] = ust_O_name
        pprint_vars["ust_O_name_with_extension"] = ust_O_name + G_CODE_FILE_EXTENSION
        return pprint_vars

    def parse_pprint(self, lines) -> dict:
        print("Parsing PPRINTs")

        program_counter = 0

        pprint_vars = ust_template_dict.copy()
        pprint_vars["cl_file_lines"] = self.get_cl_file_lines_amount(lines=lines)

        for line_index in range(lines.__len__()):
            cl_line = lines[line_index]
            if "PPRINT" in cl_line:
                if "PART NAME" in cl_line:
                    pprint_vars["part_name"] = self.get_cl_part_after_colon(cl_line=cl_line)
                elif "DATE TIME" in cl_line:
                    pprint_vars["date_and_time"] = self.get_cl_part_after_colon(cl_line=cl_line)
                elif "OPERATION NAME" in cl_line:
                    pprint_vars = self.write_ust_name_and_sub_data(pprint_vars=pprint_vars, cl_line=cl_line)

                elif "NC SEQUENCE NAME" in cl_line:
                    program_counter += 1
                    pprint_counter = 1

                    operation_dict = operation_template_dict.copy()

                    while "LOADTL" not in lines[line_index + pprint_counter]:
                        pprint_counter += 1

                    cl_in_prog_counter = 1
                    while "$$-> END /" not in lines[line_index + cl_in_prog_counter]:
                        cl_in_prog_counter += 1

                    operation_dict["pprints_index_start"] = line_index
                    operation_dict["pprints_index_end"] = line_index + pprint_counter
                    operation_dict["cl_line_index_start"] = line_index
                    operation_dict["cl_line_index_end"] = line_index + cl_in_prog_counter + 1

                    operation_dict["program_num"] = program_counter
                    operation_dict["program_num_iter"] = program_counter - 1

                    for sub_line_index in range(line_index, line_index + pprint_counter + 1):
                        sub_cl_line = lines[sub_line_index]

                        if "NC SEQUENCE NAME" in sub_cl_line:
                            operation_dict["operation_name"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                        elif "MACHINING TIME" in sub_cl_line:
                            operation_dict["machining_time"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                        elif "TOOL NAME" in sub_cl_line:
                            operation_dict["tool_name"] = sub_cl_line.split(sep=" : ")[1][:-1:]
                        elif "SPINDLE SPEED" in sub_cl_line:
                            operation_dict["spindle_speed"] = round(
                                float(sub_cl_line.split(sep=" : ")[1][:-1:].split(sep=" ")[0]), ndigits=2)
                        elif "CUT_FEED" in sub_cl_line:
                            operation_dict["cut_feed"] = round(float(sub_cl_line.split(sep=" : ")[1][:-1:]),
                                                               ndigits=2)
                        elif "LOADTL" in sub_cl_line:
                            right_part = sub_cl_line.split(sep=" / ")[1][:-1:]
                            if "$$->" in right_part:
                                pot_num = right_part.split(sep=" $$-> ")[0]
                                operation_dict["tool_pot_num_str"] = pot_num
                            else:
                                operation_dict["tool_pot_num_str"] = sub_cl_line.split(sep=" / ")[1][:-1:]

                        if program_counter < 10:
                            operation_dict["program_num_str"] = "0" + str(program_counter)
                        elif 10 <= program_counter < 100:
                            operation_dict["program_num_str"] = str(program_counter)

                        ust_sub_prog_name = PROGRAM_PREFIX + PROGRAM_MAIN_DIGIT + pprint_vars["ust_num_str"] + \
                                            operation_dict["program_num_str"]

                        operation_dict["program_O_name"] = ust_sub_prog_name
                        operation_dict[
                            "program_O_name_with_extension"] = ust_sub_prog_name + G_CODE_FILE_EXTENSION

                    pprint_vars["operations"].append(operation_dict)

                else:
                    continue
            else:
                continue

        pprint_vars["sum_machining_time"] = self.sum_machining_time(pprint_vars=pprint_vars)

        pprint(pprint_vars)
        return pprint_vars

    def count_operations(self):
        pass

    def parse_operation(self):
        pass
