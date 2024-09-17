from src.postOOP.config import LINE_ENDING


class Formatter:
    @staticmethod
    def get_cl_line_part_after_colon(*, cl_line: str) -> str:
        return cl_line.split(sep=" : ")[1][:-1:]

    @staticmethod
    def get_cl_line_part_after_comma(*, cl_line: str) -> str:
        return cl_line.split(sep=", ")[1][:-1:]

    @staticmethod
    def get_cl_part_after_slash(*, cl_line: str) -> str:
        return cl_line.split(sep=" / ")[1]

    @staticmethod
    def separate_cl_line_by_commas(*, cl_line: str) -> list[str]:
        return cl_line.split(sep=",")

    @staticmethod
    def trim_blanks_in_cl_list(*, cl_list: list[str]) -> list[str]:
        # for line in cl_list:
        #     line = line.strip()
        # return cl_list
        return [line.strip() for line in cl_list]

    @staticmethod
    def trim_line_connectors_in_cl_list(*, cl_list: list[str]) -> list[str]:
        for line_index in range(cl_list.__len__()):
            if cl_list[line_index][-2] == "$":
                cl_list[line_index] = cl_list[line_index].replace("$\n", "").strip()
        return cl_list

    @staticmethod
    def convert_cl_list_members_to_int_or_float(*, cl_list_or_str: list[str] | str, ndigits: int = 0):
        if type(cl_list_or_str) is list:
            for member_index in range(len(cl_list_or_str)):
                if ndigits == 0:
                    try:
                        cl_list_or_str[member_index] = int(round(float(cl_list_or_str[member_index]), ndigits=0))
                    except TypeError:
                        continue
                elif ndigits >= 1:
                    try:
                        cl_list_or_str[member_index] = round(float(cl_list_or_str[member_index]), ndigits=ndigits)
                        if cl_list_or_str[member_index] % 1 == 0:
                            cl_list_or_str[member_index] = int(cl_list_or_str[member_index])
                    except TypeError:
                        continue
                    pass
                else:
                    raise FloatingPointError
                return cl_list_or_str

        elif type(cl_list_or_str) is str:
            if ndigits == 0:
                try:
                    cl_list_or_str = int(round(float(cl_list_or_str), ndigits=0))
                    return cl_list_or_str
                except TypeError:
                    print("Type Error")
            elif ndigits >= 1:
                try:
                    cl_list_or_str = round(float(cl_list_or_str), ndigits=ndigits)
                    if cl_list_or_str % 1 == 0:
                        cl_list_or_str = int(cl_list_or_str)
                    return cl_list_or_str
                except TypeError:
                    print("Type Error")
                pass
            else:
                raise FloatingPointError

    @staticmethod
    def trim_line_wraps_in_cl_list_or_str(*, cl_list_or_str: list[str] | str) -> list[str] | str:
        result = list()
        if type(cl_list_or_str) is list:
            for cl_line in cl_list_or_str:
                if "\n" in cl_line:
                    result.append(cl_line.replace("\n", ""))

        elif type(cl_list_or_str) is str:
            result = cl_list_or_str.replace("\n", "")
        return result

    @staticmethod
    def append_line_wraps_in_cl_list_or_str(*, cl_list_or_str: list[str] | str) -> list[str] | str:
        result = list()
        if type(cl_list_or_str) is list:
            for cl_line in cl_list_or_str:
                cl_line = cl_line + "\n"
                result.append(cl_line)
        elif type(cl_list_or_str) is str:
            result = cl_list_or_str + "\n"
        return result

    @staticmethod
    def append_line_endings_in_cl_list_or_str(*, cl_list_or_str: list[str] | str) -> list[str] | str:
        result = list()
        if type(cl_list_or_str) is list:
            for cl_line in cl_list_or_str:
                cl_line = cl_line + LINE_ENDING
                result.append(cl_line)
        elif type(cl_list_or_str) is str:
            result = cl_list_or_str + LINE_ENDING
        return result

    @classmethod
    def format_cl_line(cls, *, cl_line: str, sep: str = ":", ndigits: int = 4) -> list[str, int, float]:
        if sep == ":":
            cl_line = cls.get_cl_line_part_after_colon(cl_line=cl_line)
        elif sep == "/":
            cl_line = cls.get_cl_part_after_slash(cl_line=cl_line)
        else:
            raise KeyError
        cl_list = cls.separate_cl_line_by_commas(cl_line=cl_line)
        cl_list = cls.trim_blanks_in_cl_list(cl_list=cl_list)
        cl_list = cls.convert_cl_list_members_to_int_or_float(cl_list_or_str=cl_list, ndigits=ndigits)
        return cl_list
