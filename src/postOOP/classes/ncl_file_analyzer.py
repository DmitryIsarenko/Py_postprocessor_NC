from src.postOOP.classes.lists_and_strings_operator import ListsAndStringsOperator


class NclFileAnalyzer:
    @staticmethod
    def count_cl_lines_in_cl_list(*, cl_list: list[str]) -> int:
        return len(cl_list)

    @staticmethod
    def get_index_of_occurence_in_cl_list_in_range(*, cl_list: list[str],
                                                   search_for: str,
                                                   start_index: int = 0,
                                                   end_index: int = -1) -> int:
        if cl_list:
            if start_index <= len(cl_list) and end_index <= len(cl_list):
                for index in range(start_index, end_index):
                    if search_for in cl_list[index]:
                        return index
            else:
                raise IndexError
        else:
            print(cl_list)
            raise TypeError


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
                lst_of_names.append(ListsAndStringsOperator.get_cl_line_part_after_colon(cl_line=line))
        return lst_of_names

    @staticmethod
    def get_date_time_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / DATE TIME :" in line:
                return ListsAndStringsOperator.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_detail_name_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / DATE TIME :" in line:
                return ListsAndStringsOperator.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_operation_name_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / OPERATION NAME :" in line:
                return ListsAndStringsOperator.get_cl_line_part_after_colon(cl_line=line)
        else:
            return None

    @staticmethod
    def get_machining_time_in_cl_list(cl_list: list[str]) -> str | None:
        for line in cl_list:
            if "PPRINT / MACHINING TIME :" in line:
                machin_time = ListsAndStringsOperator.get_cl_line_part_after_colon(cl_line=line)
                return ListsAndStringsOperator.convert_cl_list_members_to_int_or_float(cl_list_or_str=machin_time, ndigits=2)
        else:
            return None
