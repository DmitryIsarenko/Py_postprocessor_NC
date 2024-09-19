from src.postOOP.classes.formatter import Formatter


class PprintParser:
    @staticmethod
    def count_cl_lines_in_cl_list(*, cl_list: list[str]) -> int:
        return len(cl_list)

    @staticmethod
    def get_index_of_occurence_in_cl_list_in_range(*, cl_list: list[str],
                                                   search_for: str,
                                                   start_index: int = 0,
                                                   end_index: int) -> int:
        for line_index in range(start_index, end_index):
            if search_for in cl_list[line_index]:
                return line_index

    @staticmethod
    def count_nc_sequences_in_cl_list(*, cl_list: list[str]) -> int:
        counter = 0
        for line in cl_list:
            if "NC SEQUENCE NAME" in line:
                counter += 1
        return counter

    @staticmethod
    def get_list_of_nc_sequence_names(*, cl_list: list[str]) -> list[str]:
        lst_of_names = []
        for line in cl_list:
            if "PPRINT / NC SEQUENCE NAME :" in line:
                lst_of_names.append(Formatter.get_cl_line_part_after_colon(cl_line=line))
        return lst_of_names

    @staticmethod
    def get_date_time_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / DATE TIME :" in line:
                return Formatter.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_detail_name_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / PART NAME :" in line:
                return Formatter.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_operation_name_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / OPERATION NAME :" in line:
                return Formatter.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_work_offset(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "SET / OFSETL, " in line:
                return Formatter.get_cl_line_part_after_comma(cl_line=line).strip()
        else:
            return None

    @staticmethod
    def get_machining_time_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / MACHINING TIME :" in line:
                machin_time = Formatter.get_cl_line_part_after_colon(cl_line=line)
                return Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=machin_time,
                                                                         ndigits=2)
        else:
            return None

    @staticmethod
    def get_tool_name_in_cl_list_range(cl_list: list[str], start_index: int, end_index: int) -> str:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / TOOL NAME :" in line:
                return Formatter.get_cl_line_part_after_colon(cl_line=line)

    @staticmethod
    def get_tool_pot_in_cl_list_range(cl_list: list[str], start_index: int, end_index: int) -> str:
        for line in cl_list[start_index:end_index:1]:
            if "LOADTL /" in line:
                right_part: str = Formatter.get_cl_part_after_slash(cl_line=line)
                if " $$-> " in right_part:
                    comment_start_index = right_part.index(" $$-> ")
                    right_part = right_part[:comment_start_index:]
                right_part = Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=right_part,
                                                                               ndigits=0)
                return right_part

    @staticmethod
    def get_spindle_data_in_cl_list_range(cl_list: list[str], start_index: int, end_index: int) -> list:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / SPINDLE SPEED :" in line:
                right_part = Formatter.get_cl_line_part_after_colon(cl_line=line)
                right_part = right_part.split(sep=" ")
                right_part = Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=right_part,
                                                                               ndigits=0)
                return right_part

    @staticmethod
    def get_cut_feed_in_cl_list_range(cl_list: list[str], start_index: int, end_index: int) -> str:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / CUT_FEED :" in line:
                right_part = Formatter.get_cl_line_part_after_colon(cl_line=line)
                right_part = Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=right_part)
                return right_part

    @staticmethod
    def get_tool_type(cl_list: list[str], start_index: int, end_index: int) -> str:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / TOOL_TYPE :" in line:
                right_part = Formatter.get_cl_line_part_after_colon(cl_line=line)
                # right_part = Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=right_part)
                return right_part

