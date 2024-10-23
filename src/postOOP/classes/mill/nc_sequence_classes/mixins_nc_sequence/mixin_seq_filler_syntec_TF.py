from src.postOOP.classes.mill.nc_operation_classes.mixins_nc_operation.mixin_root import MixinRoot
from src.postOOP.classes.others.formatter import Formatter
from src.postOOP import config

""" pass into inheritance class

# def generate_nc_list(self):
#     return MixinSeqFillerFanucTF(self).generate_nc_list()

def generate_nc_head_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_head_lines()

def generate_nc_body_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_body_lines()

def generate_nc_tail_lines(self):
    return MixinSeqFillerFanucTF(self).generate_nc_tail_lines()

"""


class MixinSeqFillerSyntecTF(MixinRoot):
    def __init__(
            self,
            nc_seq_obj_for_syntec_filler,
            **kwargs,
    ):
        self.s = nc_seq_obj_for_syntec_filler
        super().__init__(**kwargs)

    # def generate_nc_list(self) -> list:
    #     nc_lines = list()
    #     nc_lines.extend(self.nc_seq_obj.nc_seq_head_lines)
    #     nc_lines.extend(self.nc_seq_obj.nc_seq_body_lines)
    #     nc_lines.extend(self.nc_seq_obj.nc_seq_tail_lines)
    #     nc_lines = Formatter.append_line_endings_in_cl_list_or_str(cl_list_or_str=nc_lines)
    #     nc_lines = Formatter.append_line_wraps_in_cl_list_or_str(cl_list_or_str=nc_lines)
    #     return nc_lines

    def generate_nc_seq_head_lines(self) -> list:
        nc_lines = [
            f"T{self.s.tool_pot}//..T{self.s.tool_pot}_{self.s.tool_name}",
            # f"(T{self.nc_seq_obj.tool_pot}//..T{self.nc_seq_obj.tool_pot}_{self.nc_seq_obj.tool_name})",
            f"(DETAIL={self.s.detail_name})",
            f"({self.s.nc_sequence_name})",
            f"(DATA={self.s.date_of_creation})",
            f"(PROG NUM: {self.s.nc_sequence_number} / {self.s.nc_sequences_count})",
            f"G{self.s.work_offset}",
            f"{config.SAFETY_LINE_DEFAULT}"
        ]
        return nc_lines

    def generate_nc_seq_body_lines(self) -> list:
        nc_lines = self.s.ncl_parser_class.parse_cl_list(nc_seq_obj=self.s)
        return nc_lines

    @staticmethod
    def generate_nc_seq_tail_lines() -> list:
        nc_lines = list()
        nc_lines.extend(config.NC_SEQUENCE_TAIL_LINES)
        return nc_lines
