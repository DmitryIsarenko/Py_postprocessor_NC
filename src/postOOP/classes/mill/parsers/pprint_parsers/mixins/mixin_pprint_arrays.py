from src.postOOP.classes.mill.nc_operation.mixins.mixin_root import MixinRoot
from src.postOOP.classes.formatter import Formatter


class MixinPprintArrays(MixinRoot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_is_array(cl_list: list[str], start_index: int, end_index: int) -> bool:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / MASSIV :" in line:
                return True
        return False

    @staticmethod
    def get_is_parameter_array(cl_list: list[str], start_index: int, end_index: int) -> bool:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / # : 1" in line:
                return True
        return False

    @staticmethod
    def get_array_copies_amount(cl_list: list[str], start_index: int, end_index: int) -> str:
        for line in cl_list[start_index:end_index:1]:
            if "PPRINT / MASSIV :" in line:
                copies_str = Formatter.get_cl_line_part_after_colon(cl_line=line)
                copies_int = Formatter.convert_cl_list_members_to_int_or_float(cl_list_or_str=copies_str)
                return copies_int
