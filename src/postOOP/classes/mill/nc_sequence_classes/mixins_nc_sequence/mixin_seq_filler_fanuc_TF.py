from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.others.formatter import Formatter
from src.postOOP import config

""" pass into inheritance class

def generate_nc_list(self):
    return MixinSeqFillerFanucTF(self).generate_nc_list()

def generate_nc_head_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_head_lines()

def generate_nc_body_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_body_lines()

def generate_nc_tail_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_tail_lines()

"""


class MixinSeqFillerFanucTF(MixinRoot):
    def __init__(
            self,
            nc_seq_obj_for_fanuc_filler,
            **kwargs,
    ):
        self.nc_seq_obj = nc_seq_obj_for_fanuc_filler
        super().__init__(**kwargs)

    def generate_nc_list(self) -> list:
        pre_percent = ["%", ]
        end_percent = ["%", ]
        nc_lines = list()
        nc_lines.extend(self.nc_seq_obj.nc_seq_head_lines)
        nc_lines.extend(self.nc_seq_obj.nc_seq_body_lines)
        nc_lines.extend(self.nc_seq_obj.nc_seq_tail_lines)

        nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)

        pre_percent.extend(nc_lines)
        all_lines = pre_percent
        all_lines.extend(end_percent)

        all_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=all_lines)
        return all_lines

    def generate_nc_head_lines(self) -> list:
        nc_lines = [
            f"{self.nc_seq_obj.nc_filename} (DETAIL={self.nc_seq_obj.detail_name})",
            f"({self.nc_seq_obj.nc_sequence_name})",
            f"(PROG NUM: {self.nc_seq_obj.nc_sequence_number} / {self.nc_seq_obj.nc_sequences_count})",
            f"(DATA={self.nc_seq_obj.date_of_creation})",
            f"(T{self.nc_seq_obj.tool_pot}_{self.nc_seq_obj.tool_name})",
            f"G{self.nc_seq_obj.work_offset}",
            f"{config.SAFETY_LINE_DEFAULT}",
        ]
        return nc_lines

    def generate_nc_body_lines(self) -> list:
        nc_lines = self.nc_seq_obj.ncl_parser_class.parse_cl_list(nc_seq_obj=self.nc_seq_obj)
        return nc_lines

    @staticmethod
    def generate_nc_tail_lines() -> list:
        nc_lines = list()
        nc_lines.extend(config.NC_SEQUENCE_TAIL_LINES)
        return nc_lines
